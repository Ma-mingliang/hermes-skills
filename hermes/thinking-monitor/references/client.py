"""
Thinking Monitor Client Module
思维监控客户端模块 - 实现思维过程监控、偏差检测、质量评估、报告生成

Usage:
    from client import ThinkingMonitor
    monitor = ThinkingMonitor()
    monitor.load_session(session_data)
    report = monitor.generate_report(format="markdown")
    print(report)
"""

import json
import re
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

# ── Configuration ──────────────────────────────────────────────────────────

DEFAULT_CONFIG = {
    "weights": {
        "logical_rigor": 0.30,
        "information_adequacy": 0.25,
        "bias_control": 0.25,
        "efficiency_fit": 0.20,
    },
    "thresholds": {
        "bias_high_warn": 2,
        "bias_med_warn": 1,
        "overthinking_score": 70,
        "premature_closure": 40,
        "min_sources": 2,
        "min_alternatives": 2,
    },
    "auto_mode": True,
    "report_format": "markdown",
    "save_scorecards": True,
}


# ── Bias Detection Patterns ────────────────────────────────────────────────

BIAS_DETECTORS = {
    "confirmation_bias": {
        "name": "确认偏差 (Confirmation Bias)",
        "severity": "high",
        "keywords_affirm": [
            r"正如(我|我们)?所[料想预期]", r"果然", r"不出所料",
            r"证实了", r"进一步确认", r"这证明了",
            r"支持.*观点",
        ],
        "keywords_oppose": [
            r"(但是|然而|不过).*例外", r"反面", r"反对",
            r"反例", r"与之矛盾", r"不利证据",
        ],
        "mitigation": "主动搜索反方证据：在得出结论前问'哪些证据会证明我错了？'",
    },
    "anchoring_effect": {
        "name": "锚定效应 (Anchoring Effect)",
        "severity": "high",
        "mitigation": "强制生成至少2个替代方案，并独立评估每个方案",
    },
    "overconfidence": {
        "name": "过度自信 (Overconfidence)",
        "severity": "high",
        "keywords": [
            r"\b(一定|肯定|绝对|毫无疑问|必然|100%|百分百)\b",
            r"\b(definitely|absolutely|certainly|undoubtedly|must be|no doubt)\b",
        ],
        "mitigation": "用概率语言替代绝对化表述，标注不确定性区域",
    },
    "availability_heuristic": {
        "name": "可用性启发 (Availability Heuristic)",
        "severity": "medium",
        "mitigation": "检查信息是否最近接触的过度影响了判断，参考长期统计数据",
    },
    "framing_effect": {
        "name": "框架效应 (Framing Effect)",
        "severity": "medium",
        "mitigation": "尝试用相反的框架重新表述问题，看结论是否改变",
    },
    "survivorship_bias": {
        "name": "幸存者偏差 (Survivorship Bias)",
        "severity": "medium",
        "mitigation": "不仅考虑成功案例，也要研究失败案例及其根本原因",
    },
    "sunk_cost_fallacy": {
        "name": "沉没成本谬误 (Sunk Cost Fallacy)",
        "severity": "medium",
        "keywords": [
            r"(已经|早已|投入了|花费了).*(时间|精力|资源|成本)",
            r"(不能|不该|不要)(白白|浪费|放弃)",
            r"都[已经]*做[了到]这[一步种个]",
        ],
        "mitigation": "只基于未来成本收益做决策，忽略已投入的沉没成本",
    },
    "hindsight_bias": {
        "name": "后见之明 (Hindsight Bias)",
        "severity": "low",
        "keywords": [
            r"(早就知|本来就应|当初).*(知道|该|应该|预料)",
            r"果然如此", r"不出所料", r"我早就说",
        ],
        "mitigation": "记录决策时的全部已知信息，事后对照评估",
    },
    "fundamental_attribution_error": {
        "name": "基本归因错误 (Fundamental Attribution Error)",
        "severity": "medium",
        "mitigation": "考虑环境/系统因素，而非仅归因于个人/Agent能力",
    },
}


# ── Detection Functions ────────────────────────────────────────────────────

def _detect_confirmation_bias(steps):
    """Detect confirmation bias via search pattern asymmetry"""
    searches = [s for s in steps if s.get("type") in ("search", "tool_call", "reasoning")]
    affirm_count = 0
    oppose_count = 0
    for step in searches:
        text = json.dumps(step, ensure_ascii=False).lower()
        for pat in BIAS_DETECTORS["confirmation_bias"]["keywords_affirm"]:
            if re.search(pat, text):
                affirm_count += 1
                break
        for pat in BIAS_DETECTORS["confirmation_bias"]["keywords_oppose"]:
            if re.search(pat, text):
                oppose_count += 1
                break
    if affirm_count >= 2 and oppose_count == 0:
        return {"bias": "confirmation_bias", "evidence": f"发现 {affirm_count} 次肯定性搜索，0 次反面搜索", "severity": "high"}
    if affirm_count >= 3 and oppose_count < affirm_count / 2:
        return {"bias": "confirmation_bias", "evidence": f"肯定性搜索 ({affirm_count}) 远超反面搜索 ({oppose_count})", "severity": "medium"}
    return None


def _detect_anchoring(steps):
    """Detect anchoring: is first proposal dominating later ones?"""
    proposals = [s for s in steps if s.get("type") in ("decision", "proposal", "solution")]
    if len(proposals) <= 1:
        return None
    first_solution = proposals[0].get("content", str(proposals[0]))
    later_refs = 0
    alternatives = 0
    for step in proposals[1:]:
        content = step.get("content", str(step))
        if first_solution[:20] in content:
            later_refs += 1
        if "alternative" in content.lower() or "备选" in content or "另一种" in content:
            alternatives += 1
    if later_refs >= 2 and alternatives < 1:
        return {"bias": "anchoring_effect", "evidence": f"首个方案被引用 {later_refs} 次，但仅有 {alternatives} 个替代方案", "severity": "high"}
    if later_refs >= 2 and alternatives < 2:
        return {"bias": "anchoring_effect", "evidence": f"首个方案权重偏高（{later_refs} 次引用），备选方案不足（{alternatives}）", "severity": "medium"}
    return None


def _detect_overconfidence(steps):
    """Detect overconfidence: absolute language without evidence"""
    overconfident_phrases = []
    evidenced = 0
    for step in steps:
        text = json.dumps(step, ensure_ascii=False).lower()
        for pat in BIAS_DETECTORS["overconfidence"]["keywords"]:
            matches = re.findall(pat, text, re.IGNORECASE)
            overconfident_phrases.extend(matches)
        if step.get("type") in ("verify", "evidence", "citation", "tool_call"):
            evidenced += 1
        if step.get("type") in ("claim", "conclusion") and evidenced < 1:
            overconfident_phrases.append("未经验证的断言")
    if len(overconfident_phrases) >= 2 and evidenced < len(overconfident_phrases):
        return {"bias": "overconfidence", "evidence": f"发现 {len(overconfident_phrases)} 个绝对化表述/未经证实的断言，仅 {evidenced} 次验证", "severity": "high"}
    if len(overconfident_phrases) >= 2:
        return {"bias": "overconfidence", "evidence": f"发现 {len(overconfident_phrases)} 个绝对化表述", "severity": "medium"}
    return None


def _detect_availability_heuristic(steps):
    """Detect availability heuristic: recency over-weighting"""
    recency_marks = []
    for step in steps:
        text = json.dumps(step, ensure_ascii=False).lower()
        if re.search(r"(最近|最新|刚刚|近期|recently|latest|just now)", text):
            recency_marks.append(step)
    if len(recency_marks) >= 3 and len(recency_marks) > len(steps) * 0.5:
        return {"bias": "availability_heuristic", "evidence": f"{len(recency_marks)} 个决策点依赖近期信息，可能忽略长期数据", "severity": "medium"}
    return None


def _detect_framing(steps):
    """Detect framing effect: single-frame language"""
    pos_keywords = [r"(优势|好处|收益|成功|增益)", r"(gain|benefit|success|advantage)"]
    neg_keywords = [r"(风险|损失|失败|劣势|负面)", r"(risk|loss|failure|disadvantage|downside)"]
    pos_count = 0
    neg_count = 0
    for step in steps:
        text = json.dumps(step, ensure_ascii=False)
        for pat in pos_keywords:
            if re.search(pat, text):
                pos_count += 1
                break
        for pat in neg_keywords:
            if re.search(pat, text):
                neg_count += 1
                break
    total = pos_count + neg_count
    if total >= 3 and (pos_count == 0 or neg_count == 0):
        frame_type = "正面" if pos_count > 0 else "负面"
        return {"bias": "framing_effect", "evidence": f"所有表述仅从{frame_type}框架出发（正{pos_count}/负{neg_count}）", "severity": "medium"}
    return None


def _detect_survivorship_bias(steps):
    """Detect survivorship bias: only success cases referenced"""
    success_refs = 0
    failure_refs = 0
    for step in steps:
        text = json.dumps(step, ensure_ascii=False).lower()
        if re.search(r"(成功|最佳实践|案例|benchmark|state.of.the.art|sota)", text):
            success_refs += 1
        if re.search(r"(失败|局限|问题|不足|limitation|failure|drawback|pitfall)", text):
            failure_refs += 1
    if success_refs >= 3 and failure_refs == 0:
        return {"bias": "survivorship_bias", "evidence": f"引用了 {success_refs} 个成功案例，0 个失败/局限案例", "severity": "medium"}
    return None


def _detect_sunk_cost(steps):
    """Detect sunk cost fallacy"""
    sunk_refs = []
    for step in steps:
        text = json.dumps(step, ensure_ascii=False).lower()
        for pat in BIAS_DETECTORS["sunk_cost_fallacy"]["keywords"]:
            if re.search(pat, text, re.IGNORECASE):
                sunk_refs.append(step.get("content", text[:100]))
                break
    if len(sunk_refs) >= 1:
        return {"bias": "sunk_cost_fallacy", "evidence": f"发现沉没成本相关表述: {'; '.join(sunk_refs[:2])}", "severity": "medium"}
    return None


def _detect_hindsight(steps):
    """Detect hindsight bias"""
    hindsight_count = 0
    for step in steps:
        text = json.dumps(step, ensure_ascii=False)
        for pat in BIAS_DETECTORS["hindsight_bias"]["keywords"]:
            if re.search(pat, text):
                hindsight_count += 1
                break
    if hindsight_count >= 2:
        return {"bias": "hindsight_bias", "evidence": f"发现 {hindsight_count} 个后见之明表述", "severity": "low"}
    return None


def _detect_attribution_error(steps):
    """Detect fundamental attribution error"""
    internal_attr = 0
    external_attr = 0
    for step in steps:
        text = json.dumps(step, ensure_ascii=False)
        if re.search(r"(Agent|模型|AI|LLM)(的)?(失误|错误|问题|失败)", text):
            internal_attr += 1
        if re.search(r"(环境|系统|上下文|指令|配置)(的)?(问题|错误|限制)", text):
            external_attr += 1
    if internal_attr >= 3 and external_attr == 0:
        return {"bias": "fundamental_attribution_error", "evidence": f"{internal_attr} 次归因于Agent本身，0 次归因于系统/环境", "severity": "medium"}
    return None


# Wire up detect functions
BIAS_DETECTORS["confirmation_bias"]["detect"] = _detect_confirmation_bias
BIAS_DETECTORS["anchoring_effect"]["detect"] = _detect_anchoring
BIAS_DETECTORS["overconfidence"]["detect"] = _detect_overconfidence
BIAS_DETECTORS["availability_heuristic"]["detect"] = _detect_availability_heuristic
BIAS_DETECTORS["framing_effect"]["detect"] = _detect_framing
BIAS_DETECTORS["survivorship_bias"]["detect"] = _detect_survivorship_bias
BIAS_DETECTORS["sunk_cost_fallacy"]["detect"] = _detect_sunk_cost
BIAS_DETECTORS["hindsight_bias"]["detect"] = _detect_hindsight
BIAS_DETECTORS["fundamental_attribution_error"]["detect"] = _detect_attribution_error


# ── Core Monitor Class ──────────────────────────────────────────────────────

class ThinkingMonitor:
    """
    思维监控器 — 实时监控和事后审计Agent思维过程

    Args:
        config_path: 配置文件路径 (JSON)，默认读取 ~/.hermes/monitoring/config.json
    """

    def __init__(self, config_path=None):
        self.config = DEFAULT_CONFIG.copy()
        self._load_config(config_path)
        self.session_data = []
        self.scorecard = {}

    def _load_config(self, config_path=None):
        if config_path is None:
            config_path = os.path.expanduser("~/.hermes/monitoring/config.json")
        try:
            if os.path.exists(config_path):
                with open(config_path, "r", encoding="utf-8") as f:
                    user_config = json.load(f)
                    for key in user_config:
                        if key in self.config and isinstance(self.config[key], dict):
                            self.config[key].update(user_config[key])
                        else:
                            self.config[key] = user_config[key]
        except Exception as e:
            print(f"[ThinkingMonitor] Warning: cannot load config: {e}, using defaults")

    def load_session(self, session_data):
        """Load session data from file path, JSON string, dict, or list"""
        if isinstance(session_data, str):
            if os.path.isfile(session_data):
                with open(session_data, "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                data = json.loads(session_data)
        else:
            data = session_data

        if isinstance(data, list):
            self.session_data = data
        elif isinstance(data, dict):
            for key in ("steps", "actions", "turns", "messages", "trace"):
                if key in data:
                    self.session_data = data[key]
                    break
            else:
                self.session_data = [data]
        else:
            self.session_data = []

    def _assess_logical_rigor(self):
        """Assess logical rigor (weight 30%)"""
        score = 85
        findings = []
        steps = self.session_data
        if not steps:
            return 0, ["无可用数据"]

        reasoning_steps = [s for s in steps if s.get("type") in ("reasoning", "thought", "analysis", "thinking")]
        if len(reasoning_steps) < 2:
            score -= 30
            findings.append("推理步骤过少，可能存在跳跃（< 2 个推理步骤）")
        elif len(reasoning_steps) < 4:
            score -= 10
            findings.append("推理步骤偏少（< 4 个推理步骤），建议展开中间步骤")

        assumptions = [s for s in steps if s.get("type") in ("assumption", "hypothesis")]
        decisions = [s for s in steps if s.get("type") in ("decision", "conclusion", "claim")]
        if len(decisions) > 0 and len(assumptions) == 0:
            score -= 15
            findings.append("决策前未显式声明假设")

        # Simple contradiction check
        topics = {}
        for s in reasoning_steps:
            content = s.get("content", str(s))
            for word in content.split()[:5]:
                key = word.lower().strip(",.!?;:")
                if len(key) > 3:
                    topics.setdefault(key, []).append(content)

        contradiction_signals = 0
        for topic, contents in topics.items():
            if len(contents) >= 2:
                has_positive = any("是" in c or "对" in c or "正确" in c for c in contents)
                has_negative = any("不" in c or "错" in c or "否" in c for c in contents)
                if has_positive and has_negative:
                    contradiction_signals += 1

        if contradiction_signals >= 2:
            score -= 15
            findings.append(f"检测到 {contradiction_signals} 处潜在矛盾（同一话题正反表述共存）")

        return max(0, min(100, score)), findings

    def _assess_information_adequacy(self):
        """Assess information adequacy (weight 25%)"""
        score = 80
        findings = []
        steps = self.session_data
        if not steps:
            return 0, ["无可用数据"]

        info_actions = [s for s in steps if s.get("type") in (
            "search", "web_search", "tool_call", "browser", "web_fetch",
            "skill_view", "read_file", "api_call", "research"
        )]

        tool_names = set()
        for s in info_actions:
            name = s.get("tool", s.get("name", s.get("type", "")))
            if name:
                tool_names.add(name)

        if len(info_actions) == 0:
            score -= 40
            findings.append("未进行任何信息收集，完全依赖已有知识")
        elif len(tool_names) < self.config["thresholds"]["min_sources"]:
            score -= 20
            findings.append(f"信息源偏少（{len(tool_names)} 个来源），建议至少 {self.config['thresholds']['min_sources']} 个独立源")
        elif len(tool_names) >= 3:
            score += 5
            findings.append(f"信息源充足（{len(tool_names)} 个来源）")

        verifications = [s for s in steps if s.get("type") in ("verify", "validation", "cross_check")]
        claims = [s for s in steps if s.get("type") in ("claim", "conclusion", "assertion")]
        if len(claims) > len(verifications) + 1:
            score -= 10
            findings.append(f"声明({len(claims)})与验证({len(verifications)})比例不平衡")

        unknown_declarations = [s for s in steps if s.get("type") in ("uncertainty", "unknown", "limitation", "gap")]
        if len(unknown_declarations) == 0 and len(steps) > 5:
            score -= 5
            findings.append("未显式标注不确定性区域或知识盲区")

        return max(0, min(100, score)), findings

    def _assess_bias_control(self):
        """Assess bias control (weight 25%)"""
        score = 90
        findings = []
        detected_biases = []
        steps = self.session_data
        if not steps:
            return 0, ["无可用数据"], []

        for bias_key, detector in BIAS_DETECTORS.items():
            result = detector["detect"](steps)
            if result:
                detected_biases.append(result)
                penalty = 15 if result["severity"] == "high" else 10 if result["severity"] == "medium" else 5
                score -= penalty
                findings.append(f"⚠️ {detector['name']}: {result['evidence']}")
                findings.append(f"   缓解建议: {detector['mitigation']}")

        high_count = sum(1 for b in detected_biases if b["severity"] == "high")
        med_count = sum(1 for b in detected_biases if b["severity"] == "medium")

        if high_count >= self.config["thresholds"]["bias_high_warn"]:
            findings.insert(0, f"🔴 检测到 {high_count} 个高严重度偏差，建议阻断并自我纠正")
        elif med_count >= self.config["thresholds"]["bias_med_warn"]:
            findings.insert(0, f"🟡 检测到 {med_count} 个中等严重度偏差，已记录预警")

        if not detected_biases:
            findings.append("✅ 未检测到显著认知偏差")

        return max(0, min(100, score)), findings, detected_biases

    def _assess_efficiency_fit(self):
        """Assess efficiency fit (weight 20%)"""
        score = 80
        findings = []
        steps = self.session_data
        if not steps:
            return 0, ["无可用数据"]

        tool_calls = [s for s in steps if s.get("type") in ("tool_call", "browser", "search", "terminal")]
        reasoning = [s for s in steps if s.get("type") in ("reasoning", "thought", "analysis")]

        complexity = min(5, len(set(s.get("type", "") for s in steps)) / 3 + 1)

        if complexity <= 2 and len(reasoning) > 5:
            score -= 25
            findings.append(f"过度分析：低复杂度任务({int(complexity)}/5)但推理步骤过多({len(reasoning)}步)")
        elif complexity <= 2 and len(reasoning) > 3:
            score -= 10
            findings.append(f"轻微过度分析：任务较简单但推理 {len(reasoning)} 步")

        if complexity >= 4 and len(reasoning) < 3:
            score -= 25
            findings.append(f"草率判断：高复杂度任务({int(complexity)}/5)但推理步骤过少({len(reasoning)}步)")
        elif complexity >= 4 and len(reasoning) < 5:
            score -= 10
            findings.append(f"推理略显不足：复杂任务仅 {len(reasoning)} 步推理")

        if len(tool_calls) > 15:
            score -= 10
            findings.append(f"工具调用过多（{len(tool_calls)} 次），可能效率低下")
        elif len(tool_calls) <= 3 and complexity >= 3:
            score -= 5
            findings.append(f"工具调用偏少（{len(tool_calls)} 次），可能信息收集不足")

        if score >= 90:
            findings.append("✅ 思维效率与任务复杂度匹配良好")

        return max(0, min(100, score)), findings

    def evaluate(self):
        """Run full evaluation, return scorecard dict"""
        if not self.session_data:
            return {"total_score": 0, "grade": "N/A", "error": "无会话数据", "suggestions": []}

        weights = self.config["weights"]
        logical_score, logical_findings = self._assess_logical_rigor()
        info_score, info_findings = self._assess_information_adequacy()
        bias_score, bias_findings, biases = self._assess_bias_control()
        efficiency_score, efficiency_findings = self._assess_efficiency_fit()

        w = weights
        total = round(
            logical_score * w["logical_rigor"]
            + info_score * w["information_adequacy"]
            + bias_score * w["bias_control"]
            + efficiency_score * w["efficiency_fit"],
            1,
        )

        if total >= 90:
            grade = "S"
        elif total >= 80:
            grade = "A"
        elif total >= 70:
            grade = "B"
        elif total >= 60:
            grade = "C"
        else:
            grade = "D"

        suggestions = self._generate_suggestions(logical_score, info_score, bias_score, efficiency_score, biases)

        self.scorecard = {
            "total_score": total,
            "grade": grade,
            "dimensions": {
                "logical_rigor": {"score": logical_score, "weight": w["logical_rigor"], "findings": logical_findings},
                "information_adequacy": {"score": info_score, "weight": w["information_adequacy"], "findings": info_findings},
                "bias_control": {"score": bias_score, "weight": w["bias_control"], "findings": bias_findings},
                "efficiency_fit": {"score": efficiency_score, "weight": w["efficiency_fit"], "findings": efficiency_findings},
            },
            "detected_biases": biases,
            "suggestions": suggestions,
            "timestamp": datetime.now().isoformat(),
        }
        return self.scorecard

    def _generate_suggestions(self, logical_score, info_score, bias_score, efficiency_score, biases):
        """Generate optimization suggestions from scores"""
        suggestions = []

        if logical_score < 70:
            suggestions.append({"type": "logical_rigor", "priority": "high", "suggestion": "推理链条不够完整。建议使用[前提->推理->结论]结构，显式标注每一步", "practice": "在复杂推理前先列出核心假设和已知信息"})
        elif logical_score < 85:
            suggestions.append({"type": "logical_rigor", "priority": "medium", "suggestion": "推理可进一步完善，注意中间步骤不要跳跃", "practice": "问自己：从A到B，我跳过了什么？"})

        if info_score < 70:
            suggestions.append({"type": "information", "priority": "high", "suggestion": "信息收集不足。关键决策前使用至少2个独立信息源进行三角验证", "practice": "在信息搜索后先问：还有什么我不知道的？并主动寻找盲区"})
        elif info_score < 85:
            suggestions.append({"type": "information", "priority": "medium", "suggestion": "考虑增加信息源多样性，对关键事实进行交叉验证", "practice": "每次发现重要信息后，用另一个来源验证"})

        if bias_score < 70:
            bias_names = [b.get("bias", "未知偏差") for b in biases]
            suggestions.append({"type": "bias", "priority": "high", "suggestion": f"检测到认知偏差: {', '.join(bias_names)}。运行偏差自检清单", "practice": "对每个重要判断，主动思考反方观点（Steelman对手论证）"})
        elif biases:
            suggestions.append({"type": "bias", "priority": "medium", "suggestion": f"发现 {len(biases)} 个潜在偏差，建议在决策前运行快速自检", "practice": "使用思维快速检查清单：反方观点、信息来源、假设验证"})

        if efficiency_score < 70:
            eff_findings = str(self.scorecard.get("dimensions", {}).get("efficiency_fit", {}).get("findings", []))
            if "过度分析" in eff_findings:
                suggestions.append({"type": "efficiency", "priority": "high", "suggestion": "存在过度分析倾向。先定义任务范围，避免无限深入", "practice": "在开始前评估任务复杂度（1-5级），设定期望分析深度"})
            else:
                suggestions.append({"type": "efficiency", "priority": "high", "suggestion": "分析深度不足。复杂任务需要更多推理步骤和验证", "practice": "对复杂任务使用[假设->验证->修正]循环"})

        suggestions.append({"type": "mindset", "priority": "low", "suggestion": "可选思维升级方法", "practices": [{"name": "红队思维 (Red Teaming)", "how": "扮演挑剔的审核者，寻找方案最薄弱处"}, {"name": "预检验证 (Pre-mortem)", "how": "假设项目已失败，反向追溯根本原因"}, {"name": "钢铁人论证 (Steelmanning)", "how": "构建对手观点最强的版本来检验己方论证"}]})

        return suggestions

    def generate_report(self, fmt="markdown"):
        """Generate formatted report"""
        if not self.scorecard:
            self.evaluate()

        sc = self.scorecard
        if sc.get("error"):
            return f"[ThinkingMonitor] Error: {sc['error']}"

        if fmt == "json":
            return json.dumps(sc, ensure_ascii=False, indent=2)

        total = sc["total_score"]
        grade = sc["grade"]
        dims = sc["dimensions"]
        biases = sc.get("detected_biases", [])
        suggestions = sc.get("suggestions", [])

        if fmt == "text":
            return self._format_text(total, grade, dims, biases, suggestions)
        return self._format_markdown(total, grade, dims, biases, suggestions)

    def _format_text(self, total, grade, dims, biases, suggestions):
        dim_labels = {"logical_rigor": "逻辑严谨性", "information_adequacy": "信息充分性", "bias_control": "偏差控制", "efficiency_fit": "效率适配"}
        lines = []
        lines.append("=" * 50)
        lines.append("        思维质量评分卡 (Thinking Quality Scorecard)")
        lines.append("=" * 50)
        lines.append(f"评估时间: {self.scorecard.get('timestamp', 'N/A')}")
        lines.append(f"\n📊 总分：{total}/100（等级：{grade}）\n")
        lines.append("-" * 50)
        lines.append(f"{'维度':<20} {'得分':<10} {'权重':<8}")
        lines.append("-" * 50)
        for key, label in dim_labels.items():
            d = dims.get(key, {})
            lines.append(f"{label:<20} {d.get('score', 'N/A'):<10} {d.get('weight', 0)*100:.0f}%")
        lines.append("-" * 50)
        lines.append(f"{'加权总分':<20} {total:<10}")
        lines.append("")
        for key, label in dim_labels.items():
            d = dims.get(key, {})
            findings = d.get("findings", [])
            if findings:
                lines.append(f"\n  [{label}] (得分: {d.get('score', 'N/A')})")
                for f in findings:
                    lines.append(f"    {f}")
        if biases:
            lines.append(f"\n{'─' * 50}")
            lines.append(f"偏差检测结果 ({len(biases)} 个):")
            for b in biases:
                sev = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(b.get("severity", ""), "⚪")
                lines.append(f"  {sev} {b.get('bias', '')}: {b.get('evidence', '')}")
        high_priority = [s for s in suggestions if s.get("priority") == "high"]
        if high_priority:
            lines.append(f"\n{'─' * 50}")
            lines.append("🔧 关键优化建议:")
            for i, s in enumerate(high_priority, 1):
                lines.append(f"  {i}. [{s.get('type', '')}] {s.get('suggestion', '')}")
                if s.get("practice"):
                    lines.append(f"     实践: {s['practice']}")
        lines.append("\n" + "=" * 50)
        return "\n".join(lines)

    def _format_markdown(self, total, grade, dims, biases, suggestions):
        dim_labels = {"logical_rigor": "🧠 逻辑严谨性", "information_adequacy": "📚 信息充分性", "bias_control": "🛡️ 偏差控制", "efficiency_fit": "⚡ 效率适配"}
        grade_emoji = {"S": "🏆", "A": "⭐", "B": "✅", "C": "⚠️", "D": "🔴"}.get(grade, "")
        lines = []
        lines.append("# 思维质量评分卡 (Thinking Quality Scorecard)")
        lines.append(f"\n> 评估时间: `{self.scorecard.get('timestamp', 'N/A')}`\n")
        lines.append(f"## 📊 总分：**{total}/100** {grade_emoji} 等级：**{grade}**\n")
        lines.append("| 维度 | 得分 | 权重 | 加权 |")
        lines.append("|------|------|------|------|")
        for key, label in dim_labels.items():
            d = dims.get(key, {})
            s = d.get("score", 0)
            w = d.get("weight", 0)
            lines.append(f"| {label} | {s}/100 | {w*100:.0f}% | {s*w:.1f} |")
        lines.append("")
        for key, label in dim_labels.items():
            d = dims.get(key, {})
            findings = d.get("findings", [])
            if findings:
                score_val = d.get("score", 0)
                status = "✅" if score_val >= 80 else "⚠️" if score_val >= 60 else "❌"
                lines.append(f"### {status} {label} ({score_val}/100)")
                for f in findings:
                    lines.append(f"- {f}")
                lines.append("")
        if biases:
            lines.append("## 🔍 偏差检测结果\n")
            for b in biases:
                sev = {"high": "🔴 高", "medium": "🟡 中", "low": "🟢 低"}.get(b.get("severity", ""), "⚪")
                lines.append(f"- **{sev}** | {b.get('bias', '')}: {b.get('evidence', '')}")
        if suggestions:
            lines.append("\n## 💡 优化建议\n")
            for s in suggestions:
                if s.get("type") == "mindset":
                    lines.append("### 🧘 思维模式建议")
                    for p in s.get("practices", []):
                        lines.append(f"- **{p.get('name', '')}**: {p.get('how', '')}")
                else:
                    pri = s.get("priority", "medium")
                    pri_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(pri, "")
                    lines.append(f"- {pri_icon} **[{s.get('type', '')}]** {s.get('suggestion', '')}")
                    if s.get("practice"):
                        lines.append(f"  - 💪 实践: {s['practice']}")
            lines.append("")
        return "\n".join(lines)

    def save_scorecard(self, session_id=""):
        """Save scorecard to ~/.hermes/monitoring/scorecards/"""
        if not self.scorecard:
            self.evaluate()
        base_dir = os.path.expanduser("~/.hermes/monitoring/scorecards")
        today = datetime.now().strftime("%Y-%m-%d")
        dir_path = os.path.join(base_dir, today)
        os.makedirs(dir_path, exist_ok=True)
        session_id = session_id or datetime.now().strftime("%H%M%S")
        filename = f"session_{session_id}.json"
        filepath = os.path.join(dir_path, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.scorecard, f, ensure_ascii=False, indent=2)
        index_path = os.path.join(base_dir, "index.json")
        index = []
        if os.path.exists(index_path):
            try:
                with open(index_path, "r", encoding="utf-8") as f:
                    index = json.load(f)
            except Exception:
                pass
        index.append({"file": f"{today}/{filename}", "score": self.scorecard["total_score"], "grade": self.scorecard["grade"], "timestamp": self.scorecard["timestamp"]})
        index = index[-500:]
        with open(index_path, "w", encoding="utf-8") as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
        return filepath

    @staticmethod
    def quick_check():
        """Return quick thinking self-check checklist"""
        return """
⚡ 思维快速检查 ⚡

1. 🧠 我有没有跳步？
   → 推理链是否完整？前提->推理->结论是否清晰？

2. 🛡️ 反方观点是什么？
   → 是否有确认偏差？备选方案是否被认真考虑？

3. 📚 我的信息够吗？
   → 是否使用了多源验证？是否存在知识盲区？

4. ⚡ 这个分析深度合适吗？
   → 任务复杂度(1-5)是否与分析深度匹配？

5. ❓ 我的置信度合理吗？
   → 是否使用了绝对化表述？不确定性是否被标注？

--- 偏差自检清单 ---
□ 确认偏差：我是否在回避反面证据？
□ 锚定效应：我是否过度依赖第一个方案？
□ 过度自信：我是否把假设当成确定事实？
□ 幸存者偏差：我是否只考虑了成功案例？
□ 可用性启发：我是否被近期信息过度影响？
□ 框架效应：换个方式问我还得到同样的答案吗？
□ 沉没成本：我是否因为已有投入而坚持？
□ 基本归因错误：我是否忽略了系统/环境因素？
"""


# ── Convenience API ─────────────────────────────────────────────────────────

def analyze_session(session_data, fmt="markdown"):
    """One-liner: analyze session and get report"""
    monitor = ThinkingMonitor()
    monitor.load_session(session_data)
    return monitor.generate_report(format=fmt)


def quick_scan(text_or_steps):
    """Quick bias scan on text or step list"""
    monitor = ThinkingMonitor()
    if isinstance(text_or_steps, str):
        steps = [{"type": "reasoning", "content": text_or_steps}]
    elif isinstance(text_or_steps, list):
        steps = text_or_steps
    else:
        steps = []
    monitor.load_session(steps)
    _, warnings, biases = monitor._assess_bias_control()
    return {"biases": biases, "warnings": warnings}


# ── CLI Entry Point ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python client.py <session_file.json> [--format markdown|text|json]")
        print("       python client.py --quick-check")
        sys.exit(1)
    if sys.argv[1] == "--quick-check":
        print(ThinkingMonitor.quick_check())
        sys.exit(0)
    session_file = sys.argv[1]
    fmt = "markdown"
    for i, arg in enumerate(sys.argv):
        if arg == "--format" and i + 1 < len(sys.argv):
            fmt = sys.argv[i + 1]
    result = analyze_session(session_file, format=fmt)
    print(result)
    monitor = ThinkingMonitor()
    monitor.load_session(session_file)
    monitor.evaluate()
    saved = monitor.save_scorecard()
    print(f"\n[Scorecard saved to: {saved}]")
