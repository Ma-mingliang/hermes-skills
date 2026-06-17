"""
流程思维 Skill 客户端模块
拆分事件，将任务分成细致的环节，在执行任务前进行分析和规划
"""

import os
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any


class ProcessThinking:
    """流程思维客户端类"""
    
    def __init__(self, base_dir: str = None):
        """
        初始化流程思维客户端
        
        Args:
            base_dir: 基础目录，默认为 ~/.hermes
        """
        if base_dir is None:
            base_dir = os.path.expanduser("~/.hermes")
        
        self.base_dir = base_dir
        self.processes_dir = os.path.join(base_dir, "skills", "process-thinking", "processes")
        self.templates_dir = os.path.join(base_dir, "skills", "process-thinking", "templates")
        
        # 确保目录存在
        os.makedirs(self.processes_dir, exist_ok=True)
        os.makedirs(self.templates_dir, exist_ok=True)
        
        # 初始化预定义流程模板
        self._init_templates()
    
    def _init_templates(self):
        """初始化预定义流程模板"""
        # 学习流程模板
        learning_template = {
            "name": "学习流程",
            "type": "learning",
            "description": "适用于学习新知识、新技能",
            "steps": [
                {
                    "step": 1,
                    "name": "预习",
                    "description": "提前了解学习内容",
                    "tasks": ["阅读教材", "标记疑问", "准备问题"],
                    "estimated_time": "30分钟",
                    "dependencies": []
                },
                {
                    "step": 2,
                    "name": "听课",
                    "description": "认真听讲，记录重点",
                    "tasks": ["认真听讲", "记录重点", "解决疑问"],
                    "estimated_time": "45分钟",
                    "dependencies": [1]
                },
                {
                    "step": 3,
                    "name": "练习",
                    "description": "通过练习巩固知识",
                    "tasks": ["完成作业", "巩固知识", "发现问题"],
                    "estimated_time": "60分钟",
                    "dependencies": [2]
                },
                {
                    "step": 4,
                    "name": "复习",
                    "description": "回顾和整理知识点",
                    "tasks": ["回顾笔记", "整理知识点", "查漏补缺"],
                    "estimated_time": "30分钟",
                    "dependencies": [3]
                },
                {
                    "step": 5,
                    "name": "考试",
                    "description": "检验学习效果",
                    "tasks": ["检验学习效果", "发现薄弱环节", "调整学习策略"],
                    "estimated_time": "90分钟",
                    "dependencies": [4]
                },
                {
                    "step": 6,
                    "name": "复盘",
                    "description": "分析和总结",
                    "tasks": ["分析考试结果", "总结经验教训", "改进学习方法"],
                    "estimated_time": "30分钟",
                    "dependencies": [5]
                },
                {
                    "step": 7,
                    "name": "单元测验",
                    "description": "综合检验掌握程度",
                    "tasks": ["综合检验", "确认掌握程度", "准备下一单元"],
                    "estimated_time": "60分钟",
                    "dependencies": [6]
                }
            ],
            "total_steps": 7,
            "estimated_total_time": "5小时15分钟"
        }
        
        # 开发流程模板
        development_template = {
            "name": "开发流程",
            "type": "development",
            "description": "适用于软件开发、功能实现",
            "steps": [
                {
                    "step": 1,
                    "name": "需求分析",
                    "description": "理解需求，确认目标",
                    "tasks": ["理解需求", "确认目标", "识别约束"],
                    "estimated_time": "60分钟",
                    "dependencies": []
                },
                {
                    "step": 2,
                    "name": "设计",
                    "description": "架构和接口设计",
                    "tasks": ["架构设计", "接口设计", "数据库设计"],
                    "estimated_time": "90分钟",
                    "dependencies": [1]
                },
                {
                    "step": 3,
                    "name": "编码",
                    "description": "编写和审查代码",
                    "tasks": ["编写代码", "代码审查", "单元测试"],
                    "estimated_time": "180分钟",
                    "dependencies": [2]
                },
                {
                    "step": 4,
                    "name": "测试",
                    "description": "功能和性能测试",
                    "tasks": ["功能测试", "性能测试", "安全测试"],
                    "estimated_time": "120分钟",
                    "dependencies": [3]
                },
                {
                    "step": 5,
                    "name": "部署",
                    "description": "部署上线",
                    "tasks": ["环境准备", "部署上线", "监控配置"],
                    "estimated_time": "60分钟",
                    "dependencies": [4]
                },
                {
                    "step": 6,
                    "name": "监控",
                    "description": "监控运行状态",
                    "tasks": ["性能监控", "错误监控", "用户反馈"],
                    "estimated_time": "持续",
                    "dependencies": [5]
                },
                {
                    "step": 7,
                    "name": "优化",
                    "description": "持续优化",
                    "tasks": ["性能优化", "功能优化", "用户体验优化"],
                    "estimated_time": "持续",
                    "dependencies": [6]
                }
            ],
            "total_steps": 7,
            "estimated_total_time": "约9小时"
        }
        
        # 写作流程模板
        writing_template = {
            "name": "写作流程",
            "type": "writing",
            "description": "适用于写作、博客、文章",
            "steps": [
                {
                    "step": 1,
                    "name": "选题",
                    "description": "确定写作主题",
                    "tasks": ["确定主题", "分析受众", "评估价值"],
                    "estimated_time": "30分钟",
                    "dependencies": []
                },
                {
                    "step": 2,
                    "name": "大纲",
                    "description": "设计文章结构",
                    "tasks": ["结构设计", "内容规划", "逻辑梳理"],
                    "estimated_time": "45分钟",
                    "dependencies": [1]
                },
                {
                    "step": 3,
                    "name": "初稿",
                    "description": "撰写初稿",
                    "tasks": ["撰写内容", "补充细节", "初步校对"],
                    "estimated_time": "120分钟",
                    "dependencies": [2]
                },
                {
                    "step": 4,
                    "name": "修改",
                    "description": "优化内容",
                    "tasks": ["内容优化", "结构调整", "语言润色"],
                    "estimated_time": "60分钟",
                    "dependencies": [3]
                },
                {
                    "step": 5,
                    "name": "校对",
                    "description": "最终检查",
                    "tasks": ["语法检查", "格式调整", "最终确认"],
                    "estimated_time": "30分钟",
                    "dependencies": [4]
                },
                {
                    "step": 6,
                    "name": "发布",
                    "description": "发布内容",
                    "tasks": ["选择平台", "发布内容", "推广宣传"],
                    "estimated_time": "30分钟",
                    "dependencies": [5]
                },
                {
                    "step": 7,
                    "name": "反馈",
                    "description": "收集和分析反馈",
                    "tasks": ["收集反馈", "分析效果", "持续改进"],
                    "estimated_time": "持续",
                    "dependencies": [6]
                }
            ],
            "total_steps": 7,
            "estimated_total_time": "约5小时"
        }
        
        # 保存模板
        templates = {
            "learning": learning_template,
            "development": development_template,
            "writing": writing_template
        }
        
        for template_type, template in templates.items():
            template_file = os.path.join(self.templates_dir, f"{template_type}.json")
            if not os.path.exists(template_file):
                with open(template_file, 'w', encoding='utf-8') as f:
                    json.dump(template, f, indent=2, ensure_ascii=False)
    
    def decompose_task(self, task_description: str, task_type: str = None) -> Dict:
        """
        拆分任务为多个环节
        
        Args:
            task_description: 任务描述
            task_type: 任务类型（learning/development/writing/custom）
            
        Returns:
            拆分结果
        """
        # 如果没有指定类型，尝试自动识别
        if task_type is None:
            task_type = self._identify_task_type(task_description)
        
        # 获取模板
        if task_type in ["learning", "development", "writing"]:
            template = self.get_process_template(task_type)
            process = self._customize_template(template, task_description)
        else:
            # 自定义流程
            process = self._create_custom_process(task_description)
        
        # 保存流程
        process_id = str(uuid.uuid4())[:8]
        process["id"] = process_id
        process["created_at"] = datetime.now().isoformat()
        
        process_file = os.path.join(self.processes_dir, f"{process_id}.json")
        with open(process_file, 'w', encoding='utf-8') as f:
            json.dump(process, f, indent=2, ensure_ascii=False)
        
        return process
    
    def _identify_task_type(self, task_description: str) -> str:
        """
        自动识别任务类型
        
        Args:
            task_description: 任务描述
            
        Returns:
            任务类型
        """
        task_lower = task_description.lower()
        
        # 学习相关关键词
        learning_keywords = ["学习", "学", "掌握", "了解", "研究", "study", "learn", "understand"]
        if any(keyword in task_lower for keyword in learning_keywords):
            return "learning"
        
        # 开发相关关键词
        development_keywords = ["开发", "编程", "代码", "实现", "构建", "develop", "code", "build", "implement"]
        if any(keyword in task_lower for keyword in development_keywords):
            return "development"
        
        # 写作相关关键词
        writing_keywords = ["写作", "写", "文章", "博客", "文档", "write", "blog", "article", "document"]
        if any(keyword in task_lower for keyword in writing_keywords):
            return "writing"
        
        return "custom"
    
    def _customize_template(self, template: Dict, task_description: str) -> Dict:
        """
        自定义模板
        
        Args:
            template: 模板
            task_description: 任务描述
            
        Returns:
            自定义后的流程
        """
        process = template.copy()
        process["task"] = task_description
        process["original_template"] = template["type"]
        
        # 根据任务描述调整环节
        for step in process["steps"]:
            step["task_specific"] = task_description
        
        return process
    
    def _create_custom_process(self, task_description: str) -> Dict:
        """
        创建自定义流程
        
        Args:
            task_description: 任务描述
            
        Returns:
            自定义流程
        """
        # 分析任务描述，生成环节
        steps = self._analyze_and_generate_steps(task_description)
        
        process = {
            "task": task_description,
            "type": "custom",
            "description": f"自定义流程: {task_description}",
            "steps": steps,
            "total_steps": len(steps),
            "estimated_total_time": "待评估"
        }
        
        return process
    
    def _analyze_and_generate_steps(self, task_description: str) -> List[Dict]:
        """
        分析任务描述并生成环节
        
        Args:
            task_description: 任务描述
            
        Returns:
            环节列表
        """
        # 基本环节生成逻辑
        steps = [
            {
                "step": 1,
                "name": "分析",
                "description": "分析任务需求",
                "tasks": ["理解任务目标", "识别关键要素", "确认约束条件"],
                "estimated_time": "30分钟",
                "dependencies": []
            },
            {
                "step": 2,
                "name": "规划",
                "description": "制定执行计划",
                "tasks": ["制定计划", "分配资源", "设定时间"],
                "estimated_time": "30分钟",
                "dependencies": [1]
            },
            {
                "step": 3,
                "name": "执行",
                "description": "执行任务",
                "tasks": ["按计划执行", "记录进度", "处理问题"],
                "estimated_time": "待评估",
                "dependencies": [2]
            },
            {
                "step": 4,
                "name": "检查",
                "description": "检查执行结果",
                "tasks": ["检查结果", "识别问题", "评估质量"],
                "estimated_time": "30分钟",
                "dependencies": [3]
            },
            {
                "step": 5,
                "name": "优化",
                "description": "优化和改进",
                "tasks": ["总结经验", "改进方法", "持续优化"],
                "estimated_time": "30分钟",
                "dependencies": [4]
            }
        ]
        
        return steps
    
    def get_process_template(self, process_type: str) -> Dict:
        """
        获取预定义流程模板
        
        Args:
            process_type: 流程类型（learning/development/writing）
            
        Returns:
            流程模板
        """
        template_file = os.path.join(self.templates_dir, f"{process_type}.json")
        
        if os.path.exists(template_file):
            with open(template_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return None
    
    def create_custom_process(self, name: str, steps: List[Dict]) -> Dict:
        """
        创建自定义流程
        
        Args:
            name: 流程名称
            steps: 环节列表
            
        Returns:
            自定义流程
        """
        process = {
            "name": name,
            "type": "custom",
            "description": f"自定义流程: {name}",
            "steps": steps,
            "total_steps": len(steps),
            "created_at": datetime.now().isoformat()
        }
        
        # 保存流程
        process_id = str(uuid.uuid4())[:8]
        process["id"] = process_id
        
        process_file = os.path.join(self.processes_dir, f"{process_id}.json")
        with open(process_file, 'w', encoding='utf-8') as f:
            json.dump(process, f, indent=2, ensure_ascii=False)
        
        return process
    
    def execute_process(self, process: Dict, start_step: int = 1) -> Dict:
        """
        执行流程
        
        Args:
            process: 流程定义
            start_step: 开始环节
            
        Returns:
            执行结果
        """
        execution_result = {
            "process_id": process.get("id"),
            "process_name": process.get("name"),
            "start_step": start_step,
            "start_time": datetime.now().isoformat(),
            "steps_status": [],
            "current_step": start_step,
            "completed": False
        }
        
        # 初始化环节状态
        for step in process["steps"]:
            step_status = {
                "step": step["step"],
                "name": step["name"],
                "status": "pending" if step["step"] >= start_step else "completed",
                "start_time": None,
                "end_time": None,
                "notes": []
            }
            execution_result["steps_status"].append(step_status)
        
        return execution_result
    
    def optimize_process(self, process: Dict, feedback: Dict) -> Dict:
        """
        优化流程
        
        Args:
            process: 流程定义
            feedback: 反馈信息
            
        Returns:
            优化后的流程
        """
        optimized_process = process.copy()
        
        # 根据反馈优化流程
        if "problematic_steps" in feedback:
            for step_num in feedback["problematic_steps"]:
                for step in optimized_process["steps"]:
                    if step["step"] == step_num:
                        step["needs_improvement"] = True
                        step["feedback"] = feedback.get("details", {}).get(str(step_num), "")
        
        if "suggestions" in feedback:
            optimized_process["optimization_suggestions"] = feedback["suggestions"]
        
        optimized_process["optimized_at"] = datetime.now().isoformat()
        
        return optimized_process
    
    def get_process_by_id(self, process_id: str) -> Optional[Dict]:
        """
        根据ID获取流程
        
        Args:
            process_id: 流程ID
            
        Returns:
            流程定义
        """
        process_file = os.path.join(self.processes_dir, f"{process_id}.json")
        
        if os.path.exists(process_file):
            with open(process_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return None
    
    def list_processes(self) -> List[Dict]:
        """
        列出所有流程
        
        Returns:
            流程列表
        """
        processes = []
        
        for filename in os.listdir(self.processes_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(self.processes_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    process = json.load(f)
                    processes.append({
                        "id": process.get("id"),
                        "name": process.get("name"),
                        "type": process.get("type"),
                        "total_steps": process.get("total_steps"),
                        "created_at": process.get("created_at")
                    })
        
        return processes
    
    def format_process(self, process: Dict, format: str = "text") -> str:
        """
        格式化流程
        
        Args:
            process: 流程定义
            format: 输出格式（text/json/markdown）
            
        Returns:
            格式化的流程
        """
        if format == "json":
            return json.dumps(process, indent=2, ensure_ascii=False)
        
        elif format == "markdown":
            return self._format_markdown(process)
        
        else:  # text
            return self._format_text(process)
    
    def _format_text(self, process: Dict) -> str:
        """格式化为文本"""
        lines = []
        lines.append(f"任务: {process.get('task', process.get('name', ''))}")
        lines.append(f"类型: {process.get('type', '')}")
        lines.append(f"描述: {process.get('description', '')}")
        lines.append(f"总环节数: {process.get('total_steps', 0)}")
        lines.append(f"预计总时间: {process.get('estimated_total_time', '')}")
        lines.append("")
        lines.append("流程环节:")
        
        for step in process.get("steps", []):
            lines.append(f"  {step['step']}. {step['name']}")
            lines.append(f"     描述: {step['description']}")
            lines.append(f"     任务: {', '.join(step['tasks'])}")
            lines.append(f"     预计时间: {step['estimated_time']}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _format_markdown(self, process: Dict) -> str:
        """格式化为Markdown"""
        lines = []
        lines.append(f"# {process.get('task', process.get('name', ''))}")
        lines.append("")
        lines.append(f"**类型**: {process.get('type', '')}")
        lines.append(f"**描述**: {process.get('description', '')}")
        lines.append(f"**总环节数**: {process.get('total_steps', 0)}")
        lines.append(f"**预计总时间**: {process.get('estimated_total_time', '')}")
        lines.append("")
        lines.append("## 流程环节")
        lines.append("")
        
        for step in process.get("steps", []):
            lines.append(f"### {step['step']}. {step['name']}")
            lines.append(f"")
            lines.append(f"**描述**: {step['description']}")
            lines.append(f"**预计时间**: {step['estimated_time']}")
            lines.append(f"")
            lines.append("**任务**:")
            for task in step['tasks']:
                lines.append(f"- {task}")
            lines.append("")
        
        return "\n".join(lines)


# 全局实例
_process_thinking = None


def get_process_thinking() -> ProcessThinking:
    """获取流程思维客户端单例"""
    global _process_thinking
    if _process_thinking is None:
        _process_thinking = ProcessThinking()
    return _process_thinking


# 便捷函数
def decompose_task(task_description: str, task_type: str = None) -> Dict:
    """拆分任务为多个环节"""
    return get_process_thinking().decompose_task(task_description, task_type)


def get_process_template(process_type: str) -> Dict:
    """获取预定义流程模板"""
    return get_process_thinking().get_process_template(process_type)


def create_custom_process(name: str, steps: List[Dict]) -> Dict:
    """创建自定义流程"""
    return get_process_thinking().create_custom_process(name, steps)


def execute_process(process: Dict, start_step: int = 1) -> Dict:
    """执行流程"""
    return get_process_thinking().execute_process(process, start_step)


def optimize_process(process: Dict, feedback: Dict) -> Dict:
    """优化流程"""
    return get_process_thinking().optimize_process(process, feedback)


def get_process_by_id(process_id: str) -> Optional[Dict]:
    """根据ID获取流程"""
    return get_process_thinking().get_process_by_id(process_id)


def list_processes() -> List[Dict]:
    """列出所有流程"""
    return get_process_thinking().list_processes()


def format_process(process: Dict, format: str = "text") -> str:
    """格式化流程"""
    return get_process_thinking().format_process(process, format)
