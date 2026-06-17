"""
Reasoning Trace 客户端模块
记录AI推理过程，支持事后查询和用户修改，与Hermes记忆系统结合实现持续改进
"""

import os
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any


class ReasoningTrace:
    """Reasoning Trace 客户端类"""
    
    def __init__(self, base_dir: str = None):
        """
        初始化 Reasoning Trace 客户端
        
        Args:
            base_dir: 基础目录，默认为 ~/.hermes
        """
        if base_dir is None:
            base_dir = os.path.expanduser("~/.hermes")
        
        self.base_dir = base_dir
        self.traces_dir = os.path.join(base_dir, "traces")
        self.modifications_dir = os.path.join(base_dir, "skills", "reasoning-trace", "modifications")
        
        # 确保目录存在
        os.makedirs(self.traces_dir, exist_ok=True)
        os.makedirs(self.modifications_dir, exist_ok=True)
        
        # 当前trace
        self.current_trace = None
        self.current_task_id = None
    
    def start(self, task_id: str = None, description: str = "") -> str:
        """
        开始记录推理过程
        
        Args:
            task_id: 任务ID，如果不提供则自动生成
            description: 任务描述
            
        Returns:
            任务ID
        """
        if task_id is None:
            task_id = f"task_{uuid.uuid4().hex[:8]}"
        
        self.current_task_id = task_id
        self.current_trace = {
            "task_id": task_id,
            "timestamp": datetime.now().isoformat(),
            "description": description,
            "steps": [],
            "result": None,
            "user_feedback": None,
            "modifications": []
        }
        
        return task_id
    
    def step(self, step_type: str, content: str, confidence: float = 1.0, metadata: Dict = None) -> int:
        """
        记录推理步骤
        
        Args:
            step_type: 步骤类型 (reasoning/decision/assumption/conclusion)
            content: 步骤内容
            confidence: 置信度 (0-1)
            metadata: 元数据
            
        Returns:
            步骤编号
        """
        if self.current_trace is None:
            raise ValueError("请先调用 start() 开始记录")
        
        step_num = len(self.current_trace["steps"]) + 1
        
        step_data = {
            "step": step_num,
            "type": step_type,
            "content": content,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.current_trace["steps"].append(step_data)
        
        return step_num
    
    def end(self, result: str = "success") -> Dict:
        """
        结束记录并保存
        
        Args:
            result: 任务结果 (success/failure/partial)
            
        Returns:
            完整的trace数据
        """
        if self.current_trace is None:
            raise ValueError("请先调用 start() 开始记录")
        
        self.current_trace["result"] = result
        self.current_trace["end_timestamp"] = datetime.now().isoformat()
        
        # 保存到文件
        trace_data = self.current_trace
        self._save_trace(trace_data)
        
        # 重置当前trace
        self.current_trace = None
        self.current_task_id = None
        
        return trace_data
    

    def cleanup(self, keep_days: int = 30, keep_important: bool = True, 
                keep_with_modifications: bool = True) -> Dict:
        """
        清理旧的trace文件
        
        Args:
            keep_days: 保留天数
            keep_important: 是否保留标记为重要的trace
            keep_with_modifications: 是否保留有修改意见的trace
            
        Returns:
            清理结果统计
        """
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.now() - timedelta(days=keep_days)
        
        stats = {
            "total_files": 0,
            "deleted_files": 0,
            "kept_files": 0,
            "important_files": 0,
            "modification_files": 0,
            "freed_space_kb": 0
        }
        
        # 遍历所有日期目录
        for date_dir in os.listdir(self.traces_dir):
            date_path = os.path.join(self.traces_dir, date_dir)
            
            # 跳过非日期目录
            if not os.path.isdir(date_path):
                continue
            
            try:
                dir_date = datetime.strptime(date_dir, "%Y-%m-%d")
            except ValueError:
                continue
            
            # 如果目录日期在截止日期之后，跳过
            if dir_date >= cutoff_date:
                continue
            
            # 遍历目录中的文件
            for filename in os.listdir(date_path):
                if not filename.endswith('.json'):
                    continue
                
                file_path = os.path.join(date_path, filename)
                stats["total_files"] += 1
                
                # 读取trace数据
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        trace_data = json.load(f)
                except:
                    continue
                
                # 检查是否应该保留
                should_keep = False
                
                # 保留标记为重要的trace
                if keep_important and trace_data.get("important", False):
                    should_keep = True
                    stats["important_files"] += 1
                
                # 保留有修改意见的trace
                if keep_with_modifications and trace_data.get("modifications"):
                    should_keep = True
                    stats["modification_files"] += 1
                
                # 删除或保留
                if should_keep:
                    stats["kept_files"] += 1
                else:
                    # 获取文件大小
                    file_size = os.path.getsize(file_path)
                    stats["freed_space_kb"] += file_size / 1024
                    
                    # 删除文件
                    os.remove(file_path)
                    stats["deleted_files"] += 1
            
            # 如果目录为空，删除目录
            if not os.listdir(date_path):
                os.rmdir(date_path)
        
        return stats
    
    def mark_important(self, task_id: str) -> bool:
        """
        标记trace为重要
        
        Args:
            task_id: 任务ID
            
        Returns:
            是否成功
        """
        trace_data = self.get(task_id)
        if trace_data:
            trace_data["important"] = True
            self._update_trace(trace_data)
            return True
        return False
    
    def unmark_important(self, task_id: str) -> bool:
        """
        取消trace的重要标记
        
        Args:
            task_id: 任务ID
            
        Returns:
            是否成功
        """
        trace_data = self.get(task_id)
        if trace_data:
            trace_data["important"] = False
            self._update_trace(trace_data)
            return True
        return False
    
    def get_storage_stats(self) -> Dict:
        """
        获取存储统计信息
        
        Returns:
            存储统计信息
        """
        stats = {
            "traces": {
                "total_files": 0,
                "total_size_kb": 0,
                "date_dirs": 0,
                "oldest_date": None,
                "newest_date": None
            },
            "modifications": {
                "total_files": 0,
                "total_size_kb": 0
            }
        }
        
        # 统计traces目录
        if os.path.exists(self.traces_dir):
            for date_dir in os.listdir(self.traces_dir):
                date_path = os.path.join(self.traces_dir, date_dir)
                
                if os.path.isdir(date_path):
                    stats["traces"]["date_dirs"] += 1
                    
                    # 更新日期范围
                    try:
                        dir_date = datetime.strptime(date_dir, "%Y-%m-%d")
                        if stats["traces"]["oldest_date"] is None or dir_date < stats["traces"]["oldest_date"]:
                            stats["traces"]["oldest_date"] = dir_date
                        if stats["traces"]["newest_date"] is None or dir_date > stats["traces"]["newest_date"]:
                            stats["traces"]["newest_date"] = dir_date
                    except:
                        pass
                    
                    # 统计文件
                    for filename in os.listdir(date_path):
                        if filename.endswith('.json'):
                            file_path = os.path.join(date_path, filename)
                            stats["traces"]["total_files"] += 1
                            stats["traces"]["total_size_kb"] += os.path.getsize(file_path) / 1024
        
        # 统计modifications目录
        if os.path.exists(self.modifications_dir):
            for filename in os.listdir(self.modifications_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(self.modifications_dir, filename)
                    stats["modifications"]["total_files"] += 1
                    stats["modifications"]["total_size_kb"] += os.path.getsize(file_path) / 1024
        
        return stats





    def verify_decision(self, decision: str, verification_questions: List[str] = None, 
                       context: Dict = None) -> Dict:
        """
        验证决策
        
        Args:
            decision: 决策内容
            verification_questions: 验证问题列表
            context: 上下文信息（包含之前的分析、反例等）
            
        Returns:
            验证结果
        """
        if verification_questions is None:
            verification_questions = [
                "有没有反例？",
                "一定是对的吗？",
                "如果错了会怎样？"
            ]
        
        verification_result = {
            "decision": decision,
            "questions": verification_questions,
            "answers": [],
            "counterexamples": [],
            "consistent": True,
            "needs_revision": False,
            "timestamp": datetime.now().isoformat()
        }
        
        # 记录验证过程
        if self.current_trace:
            self.step("verification", f"开始验证决策: {decision}")
        
        # 分析决策中的关键词
        decision_keywords = decision.lower().split()
        
        # 检查是否有反例
        if context and "counterexamples" in context:
            for counterexample in context["counterexamples"]:
                # 检查反例是否适用于当前决策
                if self._check_counterexample_applies(decision, counterexample):
                    verification_result["counterexamples"].append(counterexample)
                    verification_result["consistent"] = False
                    verification_result["needs_revision"] = True
        
        # 检查是否与之前的分析一致
        if context and "previous_analysis" in context:
            consistency_check = self.check_consistency(decision, context["previous_analysis"])
            if not consistency_check["consistent"]:
                verification_result["consistent"] = False
                verification_result["needs_revision"] = True
                verification_result["answers"].append({
                    "question": "与之前的分析一致吗？",
                    "answer": "不一致",
                    "details": consistency_check["conflicts"]
                })
        
        # 记录验证结果
        if self.current_trace:
            if verification_result["needs_revision"]:
                self.step("verification_result", f"决策需要修正: 发现{len(verification_result['counterexamples'])}个反例")
            else:
                self.step("verification_result", f"决策验证通过: 无反例，与分析一致")
        
        return verification_result
    
    def _check_counterexample_applies(self, decision: str, counterexample: Dict) -> bool:
        """
        检查反例是否适用于当前决策
        
        Args:
            decision: 当前决策
            counterexample: 反例信息
            
        Returns:
            反例是否适用
        """
        # 获取反例的关键信息
        counterexample_desc = counterexample.get("description", "").lower()
        counterexample_type = counterexample.get("type", "").lower()
        
        # 获取决策的关键信息
        decision_lower = decision.lower()
        
        # 检查关键词匹配
        # 例如：决策"ARIS是Agent"，反例"ARIS有CLI但是Skills"
        if "aris" in decision_lower and "aris" in counterexample_desc:
            if "agent" in decision_lower and "skills" in counterexample_desc:
                return True
            if "skills" in decision_lower and "agent" in counterexample_desc:
                return True
        
        # 通用反例检查
        if counterexample_type == "classification":
            # 分类类反例
            if any(keyword in decision_lower for keyword in ["是", "不是", "属于", "不属于"]):
                return True
        
        return False
    
    def check_consistency(self, current_decision: str, previous_analysis: str) -> Dict:
        """
        检查一致性
        
        Args:
            current_decision: 当前决策
            previous_analysis: 之前的分析
            
        Returns:
            一致性检查结果
        """
        consistency_result = {
            "current_decision": current_decision,
            "previous_analysis": previous_analysis,
            "consistent": True,
            "conflicts": [],
            "suggestions": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # 记录检查过程
        if self.current_trace:
            self.step("consistency_check", f"检查一致性: {current_decision} vs {previous_analysis}")
        
        # 提取关键词
        decision_keywords = set(current_decision.lower().split())
        analysis_keywords = set(previous_analysis.lower().split())
        
        # 检查是否存在冲突
        # 例如：决策说"ARIS是Agent"，分析说"ARIS = Skills"
        
        # 检查分类冲突
        classification_keywords = {
            "agent": ["agent", "智能体", "平台"],
            "skills": ["skills", "技能", "规则"],
            "component": ["component", "组件", "模块"]
        }
        
        decision_category = None
        analysis_category = None
        
        for category, keywords in classification_keywords.items():
            if any(keyword in decision_keywords for keyword in keywords):
                decision_category = category
            if any(keyword in analysis_keywords for keyword in keywords):
                analysis_category = category
        
        # 如果决策和分析的分类不同，则存在冲突
        if decision_category and analysis_category and decision_category != analysis_category:
            consistency_result["consistent"] = False
            consistency_result["conflicts"].append({
                "type": "classification_mismatch",
                "decision_category": decision_category,
                "analysis_category": analysis_category,
                "description": f"决策说'{current_decision}'，但分析说'{previous_analysis}'"
            })
            consistency_result["suggestions"].append(
                f"请检查：决策'{current_decision}'是否与分析'{previous_analysis}'一致"
            )
        
        # 检查逻辑冲突
        # 例如：决策说"CLI是判定标准"，分析说"CLI不能作为判定标准"
        if "cli" in decision_keywords and "cli" in analysis_keywords:
            if "是" in decision_keywords and "不能" in analysis_keywords:
                consistency_result["consistent"] = False
                consistency_result["conflicts"].append({
                    "type": "logic_mismatch",
                    "description": f"决策提到CLI是判定标准，但分析说CLI不能作为判定标准"
                })
                consistency_result["suggestions"].append(
                    "请检查：CLI是否应该作为判定标准"
                )
        
        # 记录检查结果
        if self.current_trace:
            if consistency_result["consistent"]:
                self.step("consistency_result", f"一致性检查通过: 决策与分析一致")
            else:
                self.step("consistency_result", f"一致性检查失败: 发现{len(consistency_result['conflicts'])}个冲突")
        
        return consistency_result

    def link_to_skill(self, task_id: str, skill_name: str) -> bool:
        """
        关联任务和skill
        
        Args:
            task_id: 任务ID
            skill_name: skill名称
            
        Returns:
            是否成功
        """
        trace_data = self.get(task_id)
        if trace_data:
            trace_data["linked_skill"] = skill_name
            trace_data["skill_linked_at"] = datetime.now().isoformat()
            self._update_trace(trace_data)
            
            # 更新索引
            index = self._load_index()
            if task_id in index.get("traces", {}):
                index["traces"][task_id]["linked_skill"] = skill_name
                self._save_index(index)
            
            return True
        return False
    
    def get_skill_traces(self, skill_name: str) -> List[Dict]:
        """
        获取skill的生成过程
        
        Args:
            skill_name: skill名称
            
        Returns:
            trace数据列表
        """
        traces = []
        
        # 遍历所有trace文件
        for date_dir in os.listdir(self.traces_dir):
            date_path = os.path.join(self.traces_dir, date_dir)
            if not os.path.isdir(date_path):
                continue
            
            for filename in os.listdir(date_path):
                if not filename.endswith('.json'):
                    continue
                
                file_path = os.path.join(date_path, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        trace_data = json.load(f)
                        if trace_data.get("linked_skill") == skill_name:
                            traces.append(trace_data)
                except:
                    continue
        
        return traces
    
    def save_skill_modification(self, skill_name: str, user_feedback: str, 
                               related_task_id: str = None, 
                               priority: str = "medium") -> Dict:
        """
        保存skill修改意见
        
        Args:
            skill_name: skill名称
            user_feedback: 用户反馈
            related_task_id: 相关任务ID
            priority: 优先级 (low/medium/high)
            
        Returns:
            修改意见数据
        """
        modification = {
            "skill_name": skill_name,
            "timestamp": datetime.now().isoformat(),
            "user_feedback": user_feedback,
            "related_task_id": related_task_id,
            "priority": priority,
            "applied": False
        }
        
        # 保存到modifications目录
        today = datetime.now().strftime("%Y-%m-%d")
        modification_file = os.path.join(self.modifications_dir, f"skill_{today}.json")
        
        # 读取现有修改意见
        modifications = []
        if os.path.exists(modification_file):
            with open(modification_file, 'r', encoding='utf-8') as f:
                modifications = json.load(f)
                if not isinstance(modifications, list):
                    modifications = [modifications]
        
        modifications.append(modification)
        
        # 保存
        with open(modification_file, 'w', encoding='utf-8') as f:
            json.dump(modifications, f, indent=2, ensure_ascii=False)
        
        return modification
    
    def get_skill_modifications(self, skill_name: str = None) -> List[Dict]:
        """
        获取skill修改意见
        
        Args:
            skill_name: skill名称过滤
            
        Returns:
            修改意见列表
        """
        all_modifications = []
        
        # 遍历所有修改意见文件
        for filename in os.listdir(self.modifications_dir):
            if filename.startswith('skill_') and filename.endswith('.json'):
                file_path = os.path.join(self.modifications_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        modifications = json.load(f)
                        if isinstance(modifications, list):
                            all_modifications.extend(modifications)
                        else:
                            all_modifications.append(modifications)
                except:
                    continue
        
        # 过滤
        if skill_name:
            all_modifications = [m for m in all_modifications 
                               if m.get("skill_name") == skill_name]
        
        return all_modifications
    
    def save_skill_version(self, skill_name: str, version: str, 
                          description: str = "") -> bool:
        """
        保存skill版本
        
        Args:
            skill_name: skill名称
            version: 版本号
            description: 版本描述
            
        Returns:
            是否成功
        """
        # 获取skill目录
        skill_dir = os.path.join(self.base_dir, "skills", skill_name)
        if not os.path.exists(skill_dir):
            return False
        
        # 创建版本目录
        versions_dir = os.path.join(skill_dir, "versions")
        os.makedirs(versions_dir, exist_ok=True)
        
        # 保存当前版本
        version_dir = os.path.join(versions_dir, version)
        if os.path.exists(version_dir):
            import shutil
            shutil.rmtree(version_dir)
        
        # 复制skill文件到版本目录
        import shutil
        shutil.copytree(skill_dir, version_dir, ignore=shutil.ignore_patterns('versions'))
        
        # 保存版本信息
        version_info = {
            "skill_name": skill_name,
            "version": version,
            "timestamp": datetime.now().isoformat(),
            "description": description
        }
        
        version_file = os.path.join(versions_dir, f"{version}.json")
        with open(version_file, 'w', encoding='utf-8') as f:
            json.dump(version_info, f, indent=2, ensure_ascii=False)
        
        return True
    
    def rollback_skill(self, skill_name: str, version: str) -> bool:
        """
        回滚skill到指定版本
        
        Args:
            skill_name: skill名称
            version: 版本号
            
        Returns:
            是否成功
        """
        # 获取skill目录
        skill_dir = os.path.join(self.base_dir, "skills", skill_name)
        versions_dir = os.path.join(skill_dir, "versions")
        version_dir = os.path.join(versions_dir, version)
        
        if not os.path.exists(version_dir):
            return False
        
        # 备份当前版本
        import shutil
        backup_version = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_dir = os.path.join(versions_dir, backup_version)
        shutil.copytree(skill_dir, backup_dir, ignore=shutil.ignore_patterns('versions'))
        
        # 回滚到指定版本
        # 删除当前skill文件（保留versions目录）
        for item in os.listdir(skill_dir):
            if item == 'versions':
                continue
            item_path = os.path.join(skill_dir, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
        
        # 复制版本文件到skill目录
        for item in os.listdir(version_dir):
            if item == 'versions':
                continue
            src_path = os.path.join(version_dir, item)
            dst_path = os.path.join(skill_dir, item)
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dst_path)
            else:
                shutil.copy2(src_path, dst_path)
        
        return True
    
    def get_skill_diff(self, skill_name: str, version1: str, version2: str) -> Dict:
        """
        获取skill版本差异
        
        Args:
            skill_name: skill名称
            version1: 版本1
            version2: 版本2
            
        Returns:
            差异信息
        """
        # 获取skill目录
        skill_dir = os.path.join(self.base_dir, "skills", skill_name)
        versions_dir = os.path.join(skill_dir, "versions")
        
        version1_dir = os.path.join(versions_dir, version1)
        version2_dir = os.path.join(versions_dir, version2)
        
        if not os.path.exists(version1_dir) or not os.path.exists(version2_dir):
            return {"error": "版本不存在"}
        
        # 比较文件
        diff = {
            "added": [],
            "removed": [],
            "modified": []
        }
        
        # 获取版本1的文件
        v1_files = set()
        for root, dirs, files in os.walk(version1_dir):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), version1_dir)
                v1_files.add(rel_path)
        
        # 获取版本2的文件
        v2_files = set()
        for root, dirs, files in os.walk(version2_dir):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), version2_dir)
                v2_files.add(rel_path)
        
        # 找出新增和删除的文件
        diff["added"] = list(v2_files - v1_files)
        diff["removed"] = list(v1_files - v2_files)
        
        # 找出修改的文件
        common_files = v1_files & v2_files
        for file in common_files:
            v1_path = os.path.join(version1_dir, file)
            v2_path = os.path.join(version2_dir, file)
            
            with open(v1_path, 'rb') as f1, open(v2_path, 'rb') as f2:
                if f1.read() != f2.read():
                    diff["modified"].append(file)
        
        return diff

    def get(self, task_id: str) -> Optional[Dict]:
        """
        获取指定任务的推理过程
        
        Args:
            task_id: 任务ID
            
        Returns:
            trace数据，如果不存在则返回None
        """
        # 从索引中查找
        index = self._load_index()
        if task_id in index.get("traces", {}):
            file_path = index["traces"][task_id]["file"]
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        
        # 搜索所有trace文件
        for date_dir in os.listdir(self.traces_dir):
            date_path = os.path.join(self.traces_dir, date_dir)
            if os.path.isdir(date_path):
                for filename in os.listdir(date_path):
                    if filename.endswith('.json'):
                        file_path = os.path.join(date_path, filename)
                        with open(file_path, 'r', encoding='utf-8') as f:
                            trace_data = json.load(f)
                            if trace_data.get("task_id") == task_id:
                                return trace_data
        
        return None
    
    def replay(self, task_id: str, format: str = "text") -> str:
        """
        回放推理过程
        
        Args:
            task_id: 任务ID
            format: 输出格式 (text/json/markdown)
            
        Returns:
            格式化的推理过程
        """
        trace_data = self.get(task_id)
        
        if trace_data is None:
            return f"未找到任务 {task_id} 的推理过程"
        
        if format == "json":
            return json.dumps(trace_data, indent=2, ensure_ascii=False)
        
        elif format == "markdown":
            return self._format_markdown(trace_data)
        
        else:  # text
            return self._format_text(trace_data)
    
    def save_modification(self, task_id: str, user_feedback: str, 
                         related_steps: List[int] = None, 
                         modification_type: str = "general",
                         priority: str = "medium") -> Dict:
        """
        保存用户修改意见
        
        Args:
            task_id: 任务ID
            user_feedback: 用户反馈
            related_steps: 相关步骤编号
            modification_type: 修改类型
            priority: 优先级 (low/medium/high)
            
        Returns:
            修改意见数据
        """
        modification = {
            "task_id": task_id,
            "timestamp": datetime.now().isoformat(),
            "user_feedback": user_feedback,
            "related_steps": related_steps or [],
            "modification_type": modification_type,
            "priority": priority,
            "applied": False
        }
        
        # 保存到modifications目录
        today = datetime.now().strftime("%Y-%m-%d")
        modification_file = os.path.join(self.modifications_dir, f"{today}.json")
        
        # 读取现有修改意见
        modifications = []
        if os.path.exists(modification_file):
            with open(modification_file, 'r', encoding='utf-8') as f:
                modifications = json.load(f)
                if not isinstance(modifications, list):
                    modifications = [modifications]
        
        modifications.append(modification)
        
        # 保存
        with open(modification_file, 'w', encoding='utf-8') as f:
            json.dump(modifications, f, indent=2, ensure_ascii=False)
        
        # 更新trace文件
        trace_data = self.get(task_id)
        if trace_data:
            trace_data["user_feedback"] = user_feedback
            trace_data["modifications"].append(modification)
            self._update_trace(trace_data)
        
        # 更新索引
        self._update_index(task_id, modification=modification)
        
        return modification
    
    def get_modifications(self, task_type: str = None, 
                         priority: str = None) -> List[Dict]:
        """
        获取修改意见
        
        Args:
            task_type: 任务类型过滤
            priority: 优先级过滤
            
        Returns:
            修改意见列表
        """
        all_modifications = []
        
        # 遍历所有修改意见文件
        for filename in os.listdir(self.modifications_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(self.modifications_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    modifications = json.load(f)
                    if isinstance(modifications, list):
                        all_modifications.extend(modifications)
                    else:
                        all_modifications.append(modifications)
        
        # 过滤
        if task_type:
            all_modifications = [m for m in all_modifications 
                               if m.get("modification_type") == task_type]
        
        if priority:
            all_modifications = [m for m in all_modifications 
                               if m.get("priority") == priority]
        
        return all_modifications
    
    def _save_trace(self, trace_data: Dict):
        """保存trace到文件"""
        today = datetime.now().strftime("%Y-%m-%d")
        date_dir = os.path.join(self.traces_dir, today)
        os.makedirs(date_dir, exist_ok=True)
        
        task_id = trace_data["task_id"]
        file_path = os.path.join(date_dir, f"{task_id}.json")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(trace_data, f, indent=2, ensure_ascii=False)
        
        # 更新索引
        self._update_index(task_id, file_path=file_path, trace_data=trace_data)
    
    def _update_trace(self, trace_data: Dict):
        """更新trace文件"""
        task_id = trace_data["task_id"]
        
        # 查找文件
        index = self._load_index()
        if task_id in index.get("traces", {}):
            file_path = index["traces"][task_id]["file"]
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(trace_data, f, indent=2, ensure_ascii=False)
    
    def _load_index(self) -> Dict:
        """加载索引文件"""
        index_file = os.path.join(self.traces_dir, "index.json")
        if os.path.exists(index_file):
            with open(index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"traces": {}, "modifications": {}}
    
    def _save_index(self, index: Dict):
        """保存索引文件"""
        index_file = os.path.join(self.traces_dir, "index.json")
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
    
    def _update_index(self, task_id: str, file_path: str = None, 
                     trace_data: Dict = None, modification: Dict = None):
        """更新索引"""
        index = self._load_index()
        
        if file_path and trace_data:
            index["traces"][task_id] = {
                "file": file_path,
                "timestamp": trace_data.get("timestamp"),
                "description": trace_data.get("description"),
                "result": trace_data.get("result")
            }
        
        if modification:
            if "modifications" not in index:
                index["modifications"] = {}
            index["modifications"][task_id] = modification
        
        self._save_index(index)
    
    def _format_text(self, trace_data: Dict) -> str:
        """格式化为文本"""
        lines = []
        lines.append(f"任务: {trace_data['task_id']}")
        lines.append(f"描述: {trace_data['description']}")
        lines.append(f"时间: {trace_data['timestamp']}")
        lines.append(f"结果: {trace_data['result']}")
        lines.append("")
        lines.append("推理过程:")
        
        for step in trace_data['steps']:
            lines.append(f"  {step['step']}. [{step['type']}] {step['content']}")
            if step.get('confidence'):
                lines.append(f"     置信度: {step['confidence']}")
        
        if trace_data.get('user_feedback'):
            lines.append("")
            lines.append(f"用户反馈: {trace_data['user_feedback']}")
        
        return "\n".join(lines)
    
    def _format_markdown(self, trace_data: Dict) -> str:
        """格式化为Markdown"""
        lines = []
        lines.append(f"# 推理过程: {trace_data['task_id']}")
        lines.append("")
        lines.append(f"**描述**: {trace_data['description']}")
        lines.append(f"**时间**: {trace_data['timestamp']}")
        lines.append(f"**结果**: {trace_data['result']}")
        lines.append("")
        lines.append("## 推理步骤")
        lines.append("")
        
        for step in trace_data['steps']:
            lines.append(f"### 步骤 {step['step']}: {step['type']}")
            lines.append(f"")
            lines.append(f"{step['content']}")
            if step.get('confidence'):
                lines.append(f"")
                lines.append(f"**置信度**: {step['confidence']}")
            lines.append("")
        
        if trace_data.get('user_feedback'):
            lines.append("## 用户反馈")
            lines.append("")
            lines.append(trace_data['user_feedback'])
        
        return "\n".join(lines)


# 全局实例
_trace_client = None


def get_trace_client() -> ReasoningTrace:
    """获取 Reasoning Trace 客户端单例"""
    global _trace_client
    if _trace_client is None:
        _trace_client = ReasoningTrace()
    return _trace_client


# 便捷函数
def start_trace(task_id: str = None, description: str = "") -> str:
    """开始记录推理过程"""
    return get_trace_client().start(task_id, description)


def trace_step(step_type: str, content: str, confidence: float = 1.0, 
               metadata: Dict = None) -> int:
    """记录推理步骤"""
    return get_trace_client().step(step_type, content, confidence, metadata)


def end_trace(result: str = "success") -> Dict:
    """结束记录"""
    return get_trace_client().end(result)


def get_trace(task_id: str) -> Optional[Dict]:
    """获取推理过程"""
    return get_trace_client().get(task_id)


def replay_trace(task_id: str, format: str = "text") -> str:
    """回放推理过程"""
    return get_trace_client().replay(task_id, format)


def save_modification(task_id: str, user_feedback: str, 
                     related_steps: List[int] = None,
                     modification_type: str = "general",
                     priority: str = "medium") -> Dict:
    """保存修改意见"""
    return get_trace_client().save_modification(
        task_id, user_feedback, related_steps, modification_type, priority
    )


def get_modifications(task_type: str = None, priority: str = None) -> List[Dict]:
    """获取修改意见"""
    return get_trace_client().get_modifications(task_type, priority)


# 清理相关便捷函数
def cleanup_traces(keep_days: int = 30, keep_important: bool = True) -> Dict:
    """清理旧的trace文件"""
    return get_trace_client().cleanup(keep_days, keep_important)


def mark_trace_important(task_id: str) -> bool:
    """标记trace为重要"""
    return get_trace_client().mark_important(task_id)


def unmark_trace_important(task_id: str) -> bool:
    """取消trace的重要标记"""
    return get_trace_client().unmark_important(task_id)


def get_storage_stats() -> Dict:
    """获取存储统计信息"""
    return get_trace_client().get_storage_stats()


# skill相关便捷函数
def link_task_to_skill(task_id: str, skill_name: str) -> bool:
    """关联任务和skill"""
    return get_trace_client().link_to_skill(task_id, skill_name)


def get_skill_traces(skill_name: str) -> List[Dict]:
    """获取skill的生成过程"""
    return get_trace_client().get_skill_traces(skill_name)


def save_skill_modification(skill_name: str, user_feedback: str, 
                           related_task_id: str = None) -> Dict:
    """保存skill修改意见"""
    return get_trace_client().save_skill_modification(skill_name, user_feedback, related_task_id)


def get_skill_modifications(skill_name: str = None) -> List[Dict]:
    """获取skill修改意见"""
    return get_trace_client().get_skill_modifications(skill_name)


def save_skill_version(skill_name: str, version: str, description: str = "") -> bool:
    """保存skill版本"""
    return get_trace_client().save_skill_version(skill_name, version, description)


def rollback_skill(skill_name: str, version: str) -> bool:
    """回滚skill到指定版本"""
    return get_trace_client().rollback_skill(skill_name, version)


def get_skill_diff(skill_name: str, version1: str, version2: str) -> Dict:
    """获取skill版本差异"""
    return get_trace_client().get_skill_diff(skill_name, version1, version2)


# 思维验证相关便捷函数
def verify_decision(decision: str, verification_questions: List[str] = None, 
                   context: Dict = None) -> Dict:
    """验证决策"""
    return get_trace_client().verify_decision(decision, verification_questions, context)


def check_consistency(current_decision: str, previous_analysis: str) -> Dict:
    """检查一致性"""
    return get_trace_client().check_consistency(current_decision, previous_analysis)
