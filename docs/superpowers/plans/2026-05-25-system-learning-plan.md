# 🗺️ Aligo 商旅助手 → AI Agent 系统学习计划

> **For agentic workers:** 本计划将作为你从 Java 初级开发员转型为「Python + TypeScript + Java 三语 AI Agent 开发者」的系统性学习路线图。每课产出笔记和代码并存到 `Learning/` 目录。

**目标：** 通过深入拆解 Aligo 商旅助手（多智能体旅行规划系统），系统掌握 AI Agent 开发的核心能力，成为三语初级开发者。

**架构：**  
- 第 1 阶段：环境准备 + Python 基础补强（为读懂项目打基础）
- 第 2 阶段：逐模块精读项目代码（CLI → 意图识别 → 协调器 → 记忆系统 → RAG → 工具链）
- 第 3 阶段：动手改造 + 测试驱动（三语横向扩展）
- 第 4 阶段：独立构建自己的 AI Agent 项目

**技术栈：** Python 3 · AgentScope 1.0.16 · 豆包/OpenAI API · Milvus Lite · BGE Embedding · Rich CLI · asyncio ·（后续扩展）TypeScript · Java Spring AI

---

## 📂 涉及文件总览

| 模块 | 文件 | 职责 |
|------|------|------|
| **入口** | `cli.py` | CLI 主程序，用户交互入口 |
| **配置** | `config.py` | 系统配置（LLM、RAG、熔断器） |
| **配置** | `config_agentscope.py` | AgentScope 框架初始化 |
| **编排层** | `agents/intention_agent.py` | 意图识别（LLM 语义理解） |
| **编排层** | `agents/orchestration_agent.py` | 协调器（并行调度 + 消息传递） |
| **编排层** | `agents/lazy_agent_registry.py` | 插件注册器（懒加载） |
| **记忆层** | `context/memory_manager.py` | 记忆管理器（统一接口） |
| **记忆层** | `context/short_term_memory.py` | 短期记忆（滑动窗口） |
| **记忆层** | `context/long_term_memory.py` | 长期记忆（JSON 持久化） |
| **工具层** | `utils/circuit_breaker.py` | 熔断器 |
| **工具层** | `utils/llm_resilience.py` | 重试退避 + 健康检查 |
| **工具层** | `utils/json_parser.py` | JSON 解析 |
| **工具层** | `utils/skill_loader.py` | Skill 加载器 |
| **Skill 插件** | `.claude/skills/*/script/agent.py` | 6 个子智能体实现 |
| **测试** | `tests/test_memory_system.py` | 记忆系统测试 |
| **测试** | `tests/test_intention_agent.py` | 意图识别测试 |
| **测试** | `tests/test_orchestration.py` | 协调器测试 |
| **测试** | `tests/test_cli_qa.py` | 端到端集成测试 |
| **数据** | `data/memory/*.json` | 长期记忆持久化文件 |
| **笔记输出** | `Learning/` | 每课的学习笔记 |

---

## 阶段一：环境就绪与快速热身

### 任务 1.1：确认开发环境 ✅

**文件：** 无需修改，仅检查环境

- [x] **步骤：检查 Python 版本**

```bash
python3 --version
# 期望: Python 3.10+
```

- [x] **步骤：创建虚拟环境并安装依赖**

```bash
cd /home/ljh2923/pi-projects/项目学习/travel-Agent/repo
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

期望输出：所有包安装成功，无报错

- [x] **步骤：验证项目能启动（即使无 API 密钥）**

```bash
python cli.py
```

期望：看到 Rich 风格的 CLI 界面，提示输入 API 密钥或报错信息（`API_KEY` 占位符会报错，属于正常）

- [x] **步骤：提交并 push**

```bash
git add -A && git commit -m "docs: lesson 1.1 - dev environment ready"
git push
```

---

### 任务 1.2：Python 核心语法速通（面向 Java 开发者） ✅

**学习笔记输出：** `Learning/02-Python核心语法速通.md`

本任务是为**从 Java 转 Python** 的你量身定制。只学本项目用到的语法，不学无关内容。

- [x] **步骤：变量与类型（对比 Java）**

```python
# Java:   String name = "张三";
# Python:
name: str = "张三"

# Java:   List<String> list = new ArrayList<>();
# Python:
items: list[str] = ["北京", "上海", "杭州"]

# Java:   Map<String, Object> map = new HashMap<>();
# Python:
data: dict[str, any] = {"出发地": "北京", "时间": "2026-03-11"}
```

📝 笔记要点：
- Python 无需声明类型，类型注解只做提示（运行时无强制）
- `list` / `dict` 是内置的，不需要 import
- 对比 Java 的 `ArrayList` / `HashMap`

- [x] **步骤：函数定义与类型注解**

```python
# Java: public String greet(String name) { return "Hello " + name; }
# Python:
def greet(name: str) -> str:
    return f"Hello {name}"

# 默认参数
def process_query(user_input: str, max_tokens: int = 8192) -> dict:
    return {"query": user_input, "tokens": max_tokens}
```

📝 笔记要点：
- `def` 替代 `public/private` 等访问修饰符
- `-> str` 是返回类型注解
- f-string：`f"Hello {name}"` 替代 Java 的字符串拼接/`String.format`

- [x] **步骤：类与继承（本项目核心模式）**

```python
# 本项目大量使用 AgentBase 基类
class IntentionAgent(AgentBase):     # 继承 AgentBase
    def __init__(self, name: str, model=None, **kwargs):
        super().__init__()           # 调用父类构造器
        self.name = name
        self.model = model

    async def reply(self, x):        # 覆盖父类方法
        # ... 处理逻辑
        return Msg(name=self.name, content=json.dumps({}), role="assistant")
```

📝 笔记要点：
- `class A(B)` = Java 的 `class A extends B`
- `super().__init__()` = Java 的 `super()`
- `**kwargs` = 可变关键字参数（Java 中没有直接的等价物）

- [x] **步骤：async/await 异步编程（最核心！）**

```python
# 本项目的灵魂——异步并发
import asyncio

# 定义异步函数
async def fetch_weather(city: str) -> str:
    # ... 模拟网络请求
    await asyncio.sleep(1)  # await = 等待异步操作完成
    return f"{city}: 25°C"

# 并发执行（核心模式！）
async def main():
    cities = ["北京", "上海", "杭州"]
    # asyncio.gather = 并行执行多个任务
    results = await asyncio.gather(
        fetch_weather("北京"),
        fetch_weather("上海"),
        fetch_weather("杭州"),
    )
    print(results)

# 运行
asyncio.run(main())
```

📝 笔记要点：
- `async def` = Java 中没有直接等价（类似 `CompletableFuture.supplyAsync`）
- `await` = 等待一个异步操作完成（类似 JS 的 await / Java 的 `.get()`）
- `asyncio.gather()` = 并发执行多个任务（类似 Java 的 `CompletableFuture.allOf()`）
- **本项目在 `orchestration_agent.py` 中用 `asyncio.gather()` 实现优先级并行调度**

- [x] **步骤：异常处理**

```python
# Java: try { ... } catch (Exception e) { ... } finally { ... }
# Python:
try:
    result = await agent.reply(input_data)
except json.JSONDecodeError as e:
    print(f"JSON 解析失败: {e}")
except CircuitOpenError:
    print("服务熔断，请稍后重试")
except Exception as e:
    print(f"未知错误: {e}")
finally:
    cleanup()
```

- [x] **步骤：实现本节所学内容**

**动手任务**：用 Python 写一个简单的「意图识别模拟器」

```python
# learning_challenges/simple_intention.py
import json
import asyncio

# 模拟的意图类别
INTENTIONS = {
    "plan": "行程规划",
    "query": "信息查询",
    "preference": "偏好管理",
}

async def detect_intention(user_input: str) -> dict:
    """
    模拟 LLM 意图识别（实际项目中调用大模型）
    
    Args:
        user_input: 用户输入的自然语言
    
    Returns:
        包含意图类型的字典
    """
    keywords = {
        "plan": ["规划", "安排", "去", "出差", "旅程"],
        "query": ["查询", "天气", "怎么样", "多少钱"],
        "preference": ["喜欢", "偏好", "习惯", "爱住"],
    }
    
    for intent, words in keywords.items():
        for word in words:
            if word in user_input:
                return {"intent": intent, "name": INTENTIONS[intent]}
    
    return {"intent": "unknown", "name": "未识别"}

async def main():
    """主函数"""
    test_inputs = [
        "我想去北京出差",
        "明天天气怎么样",
        "我喜欢住汉庭酒店",
        "你好啊",
    ]
    
    for inp in test_inputs:
        result = await detect_intention(inp)
        print(f"输入: {inp}")
        print(f"识别: {result['name']}")
        print("-" * 30)

if __name__ == "__main__":
    asyncio.run(main())
```

✅ **运行验证**：

```bash
python learning_challenges/simple_intention.py
# 期望输出：
# 输入: 我想去北京出差
# 识别: 行程规划
# ...
```

- [x] **步骤：撰写笔记并提交**

```bash
git add -A && git commit -m "feat: lesson 1.2 - Python core syntax"
git push
```

---

## 阶段二：逐模块精读项目代码

### 任务 2.1：入口分析 — `cli.py`

**学习笔记输出：** `Learning/03-CLI入口分析.md`

- [ ] **步骤：通读 `cli.py` 的类结构**

读文件：`cli.py`（~750行）
理解 `AligoCLI` 类的核心方法：

| 方法 | 职责 | 类比 Java |
|------|------|-----------|
| `__init__` | 初始化所有组件 | 构造器 + DI 注入 |
| `initialize_system` | 启动时懒加载初始化 | @PostConstruct |
| `process_query` | 核心处理流程 | Controller 层 |
| `run` | 事件循环 | while(true) 主循环 |

- [ ] **步骤：深入 `initialize_system` 初始化流程**

追踪初始化链路：
```
cli.py:initialize_system
  ├─ Prompt.ask("用户ID")      ← 终端输入
  ├─ init_agentscope()         ← 框架初始化
  ├─ OpenAIChatModel(...)      ← LLM 模型初始化
  ├─ MemoryManager(...)        ← 记忆管理器
  ├─ IntentionAgent(...)       ← 意图识别（预加载）
  ├─ LazyAgentRegistry(...)    ← 插件注册器（懒加载）
  └─ OrchestrationAgent(...)   ← 协调器
```

📝 **关键理解**：
- 为什么 `IntentionAgent` 必须预加载？→ 因为它是「大脑」，每个请求都要用它
- 为什么其他 Agent 用 `LazyAgentRegistry` 懒加载？→ 只有被调度到时才加载，启动快

- [ ] **步骤：深入 `process_query` 核心处理流程**

追踪请求链路（**这是整项目的灵魂流程！**）：

```
process_query(user_input)
  │
  ├─ ① 熔断检查
  │   └─ circuit_breaker.raise_if_open()
  │
  ├─ ② 准备上下文
  │   ├─ 长期记忆摘要（历史会话总结）
  │   ├─ 短期记忆（最近5轮对话）
  │   └─ 组装成 Msg 列表
  │
  ├─ ③ 意图识别（带重试）
  │   └─ intention_agent.reply(context_messages)
  │
  ├─ ④ 解析意图结果
  │   └─ json.loads(intention_result.content)
  │
  ├─ ⑤ 调度执行（带重试）
  │   └─ orchestrator.reply(intention_result)
  │
  ├─ ⑥ 解析执行结果
  │
  ├─ ⑦ 显示结果
  │   ├─ _display_agents_called()
  │   └─ _display_results()
  │
  └─ ⑧ 存入记忆
      └─ memory_manager.add_message()
```

- [ ] **步骤：动手画流程图**

用 Mermaid 或手绘方式画出 `process_query` 的完整调用链。

- [ ] **步骤：撰写笔记并提交**

```bash
git add -A && git commit -m "docs: lesson 2.1 - CLI entry analysis"
git push
```

---

### 任务 2.2：Intent Agent — 意图识别智能体

**学习笔记输出：** `Learning/04-意图识别智能体深度解析.md`

- [ ] **步骤：通读 `agents/intention_agent.py`**

重点理解：
1. **两段式输出结构**：先输出推理过程（Reasoning），再输出 JSON 决策
2. **Prompt 工程设计**：如何让 LLM 准确输出结构化结果
3. **6 类意图的区分逻辑**：看 Prompt 是怎么写的

- [ ] **步骤：理解 Prompt 结构**

```python
# intention_agent.py 中的核心部分
prompt = f"""你是一个高级意图识别专家...
【当前时间】
{current_time} {weekday}

【用户Query】
{user_query}

【对话历史上下文】
{context_str}

【可调度的子智能体 (Skills)】
{dynamic_skills_prompt}

请一步步推理...
...
输出格式：
{{
    "intentions": ["intent_1", "intent_2"],
    "reasoning": "...",
    "rewritten_query": "...",
    "schedule": {{
        "priority_1": ["agent_1", "agent_2"],
        "priority_2": ["agent_3"]
    }}
}}
```

📝 **学习要点**：
- 系统提示（System Prompt）的设计技巧
- Few-shot 示例如何帮助 LLM 理解输出格式
- 为什么需要「推理过程」+「JSON 输出」两段式结构？
- 对比：传统方法用关键词匹配 vs LLM 语义理解的优势

- [ ] **步骤：理解 AgentScope 的 AgentBase 基类**

读 `IntentionAgent` 的继承与实现：

```python
class IntentionAgent(AgentBase):
    """
    意图识别智能体
    继承自 AgentScope 的 AgentBase 基类
    """
    
    async def reply(self, x: Optional[Union[Msg, List[Msg]]] = None) -> Msg:
        """
        必须重写的方法——所有 Agent 的统一接口
        
        Args:
            x: 输入消息或消息列表
        
        Returns:
            Msg: 输出消息
        """
```

📝 **理解 AgentScope 的核心抽象**：
- 所有 Agent 都继承 `AgentBase`
- 所有 Agent 都实现 `reply(x) -> Msg` 方法
- 这就是「多智能体框架」的核心——统一的通信协议

- [ ] **步骤：模拟意图识别（无需 LLM）**

```python
# learning_challenges/simulate_intention.py
"""
模拟 IntentAgent 的处理流程，帮助你理解意图识别的工作方式
"""

QUERY_TEMPLATE = """
你是一个意图识别专家。
请分析用户查询并识别意图类别。

可识别的意图：
1. itinerary_planning - 行程规划
2. memory_query - 记忆查询
3. preference - 偏好管理
4. rag_knowledge - 知识问答
5. information_query - 信息查询
6. event_collection - 事项收集

用户输入: {user_input}

请先推理，再输出JSON。
"""

class SimulatedIntentionAgent:
    """
    模拟意图识别智能体（基于规则而非 LLM）
    帮助你理解意图识别的核心逻辑
    """
    
    def __init__(self):
        self.intent_keywords = {
            "itinerary_planning": ["规划", "安排", "去", "出差", "旅行", "从"],
            "memory_query": ["去过", "之前", "历史", "回忆", "什么时候"],
            "preference": ["喜欢", "偏好", "爱住", "习惯", "想住"],
            "rag_knowledge": ["标准", "报销", "政策", "规定", "指南"],
            "information_query": ["天气", "查询", "多少", "怎么样", "信息"],
            "event_collection": [],  # 通常和其他意图一起出现
        }
    
    def detect(self, user_input: str) -> dict:
        """
        检测用户输入的意图
        
        Args:
            user_input: 用户输入
        
        Returns:
            意图识别结果
        """
        detected = []
        
        for intent, keywords in self.intent_keywords.items():
            for kw in keywords:
                if kw in user_input:
                    detected.append(intent)
                    break
        
        if not detected:
            detected = ["event_collection"]
        
        return {
            "intentions": detected,
            "reasoning": f"检测到关键词匹配: {detected}",
            "rewritten_query": user_input,
            "schedule": {
                "priority_1": detected,
                "priority_2": ["itinerary_planning"] if "itinerary_planning" in detected else []
            }
        }


# 测试
agent = SimulatedIntentionAgent()
test_cases = [
    "我想3月11日从北京去杭州出差一周",
    "我去过哪些地方旅游",
    "我喜欢住汉庭酒店",
    "出差住宿标准是多少",
    "北京明天天气怎么样",
]

for case in test_cases:
    result = agent.detect(case)
    print(f"\n输入: {case}")
    print(f"意图: {result['intentions']}")
    print(f"优先级1: {result['schedule']['priority_1']}")
    print("-" * 40)
```

- [ ] **步骤：撰写笔记并提交**

```bash
git add -A && git commit -m "docs: lesson 2.2 - intention agent deep dive"
git push
```

---

### 任务 2.3：Orchestrator — 协调器智能体

**学习笔记输出：** `Learning/05-协调器智能体深度解析.md`

- [ ] **步骤：通读 `agents/orchestration_agent.py`**

重点理解：
1. 优先级调度逻辑：`priority_1` 先执行，`priority_2` 后执行
2. 并行执行机制：`asyncio.gather()` 并发执行同优先级的 Agent
3. Agent 间消息传递：前一个 Agent 的输出如何传递给下一个

- [ ] **步骤：追踪并行调度核心代码**

```python
# orchestration_agent.py 中的核心调度逻辑
async def _execute_agents(self, agents_to_run: list, context: str) -> list:
    """按优先级执行智能体"""
    results = []
    
    # 按优先级分组
    priority_groups = {}
    for item in agents_to_run:
        priority = item.get("priority", 1)
        priority_groups.setdefault(priority, []).append(item)
    
    # 按优先级从高到低执行
    for priority in sorted(priority_groups.keys()):
        group = priority_groups[priority]
        
        if len(group) == 1:
            # 单个 Agent 直接执行
            result = await self._run_single_agent(group[0], context)
            results.append(result)
        else:
            # 多个 Agent 并行执行！⭐
            tasks = [self._run_single_agent(item, context) for item in group]
            parallel_results = await asyncio.gather(*tasks)
            results.extend(parallel_results)
    
    return results
```

📝 **学习要点**：
- 对比 Java：`CompletableFuture.allOf()` 和 `asyncio.gather()` 的异同
- 为什么需要优先级？→ 行程规划依赖前序 Agent 的收集结果
- 并行执行如何提升性能？→ 30秒 → 15秒（-50%）

- [ ] **步骤：绘制调度执行序列图**

用 Mermaid 画出一次完整请求的 Agent 调度序列

- [ ] **步骤：撰写笔记并提交**

```bash
git add -A && git commit -m "docs: lesson 2.3 - orchestrator deep dive"
git push
```

---

### 任务 2.4：记忆系统 — 短期 + 长期记忆

**学习笔记输出：** `Learning/06-记忆系统深度解析.md`

- [ ] **步骤：通读 `context/short_term_memory.py`**

```python
class ShortTermMemory:
    """
    短期记忆——基于滑动窗口的会话级记忆
    类似人的「短期工作记忆」
    """
    
    def __init__(self, max_turns: int = 10):
        self.messages: list[dict] = []
        self.max_turns = max_turns
    
    def add_message(self, role: str, content: str, metadata: dict = None):
        """添加消息，超出 max_turns 时自动丢弃最旧的"""
        self.messages.append({...})
        if len(self.messages) > self.max_turns * 2:
            self.messages = self.messages[-(self.max_turns * 2):]
    
    def get_recent_context(self, n_turns: int = 5) -> list:
        """获取最近 n 轮对话"""
        return self.messages[-(n_turns * 2):]
```

📝 **学习要点**：
- 滑动窗口机制：为什么是最近 10 轮？→ Token 限制与上下文窗口
- 对比：Redis 实现 vs 当前的内存实现

- [ ] **步骤：通读 `context/long_term_memory.py`**

重点理解：
1. JSON 文件持久化结构
2. 偏好追加（append）vs 覆盖（override）的智能识别
3. LLM 异步总结——如何从对话中提取关键信息

```python
class LongTermMemory:
    """
    长期记忆——跨会话持久化存储
    
    数据结构：
    {
        "user_id": "default_user",
        "preferences": {"hotel_brands": ["汉庭", "如家"], ...},
        "trip_history": [
            {"start": "北京", "end": "杭州", "date": "2026-03-11", ...}
        ],
        "chat_history": [...],
        "statistics": {"total_trips": 3, ...}
    }
    """
```

- [ ] **步骤：通读 `context/memory_manager.py`**

理解如何统一管理两层记忆：

```python
class MemoryManager:
    """
    记忆管理器——统一接口
    
    职责：
    1. 同时管理短期 + 长期记忆
    2. 为 Agent 提供格式化上下文
    3. 触发 LLM 异步总结
    """
    
    def get_context_for_agent(self, long_term_summary: str = None) -> str:
        """合并两层记忆为 Agent 可读的上下文字符串"""
```

- [ ] **步骤：运行记忆系统测试**

```bash
cd /home/ljh2923/pi-projects/项目学习/travel-Agent/repo
source venv/bin/activate
python tests/test_memory_system.py
```

阅读测试代码，理解每个测试用例覆盖了什么场景。

- [ ] **步骤：动手实现——自己写一个简化版记忆管理器**

```python
# learning_challenges/simple_memory.py
"""
简化版记忆管理器——动手实现理解核心概念
"""

class SimpleShortTermMemory:
    """
    简化版短期记忆——滑动窗口
    """
    
    def __init__(self, max_turns: int = 3):
        self.messages = []
        self.max_turns = max_turns
    
    def add_message(self, role: str, content: str):
        """添加消息，超出限制时丢弃最旧"""
        self.messages.append({"role": role, "content": content})
        # 保留最近 max_turns 轮（每条消息包含 user + assistant 两条记录）
        if len(self.messages) > self.max_turns * 2:
            self.messages = self.messages[-(self.max_turns * 2):]
    
    def get_context(self) -> str:
        """获取格式化的上下文"""
        lines = []
        for msg in self.messages:
            role_cn = "用户" if msg["role"] == "user" else "助手"
            lines.append(f"{role_cn}: {msg['content']}")
        return "\n".join(lines)


class SimpleLongTermMemory:
    """
    简化版长期记忆——JSON 持久化
    """
    
    def __init__(self, filepath: str = "memory_data.json"):
        self.filepath = filepath
        self.data = self._load()
    
    def _load(self) -> dict:
        """从文件加载"""
        import os, json
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                return json.load(f)
        return {"preferences": {}, "trips": []}
    
    def save(self):
        """保存到文件"""
        import json
        with open(self.filepath, "w") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def add_preference(self, key: str, value: str, append: bool = False):
        """添加偏好"""
        if append and key in self.data["preferences"]:
            if isinstance(self.data["preferences"][key], list):
                self.data["preferences"][key].append(value)
            else:
                old = self.data["preferences"][key]
                self.data["preferences"][key] = [old, value]
        else:
            self.data["preferences"][key] = value
        self.save()


# 测试
def test_memory():
    stm = SimpleShortTermMemory(max_turns=3)
    stm.add_message("user", "我喜欢住汉庭")
    stm.add_message("assistant", "好的，已记录")
    stm.add_message("user", "我还喜欢如家")
    print("短期记忆上下文:")
    print(stm.get_context())
    
    ltm = SimpleLongTermMemory("test_memory.json")
    ltm.add_preference("hotel_brands", "汉庭")
    ltm.add_preference("hotel_brands", "如家", append=True)
    print("\n长期记忆数据:")
    print(ltm.data)
    
    import os
    os.remove("test_memory.json")

if __name__ == "__main__":
    test_memory()
```

- [ ] **步骤：撰写笔记并提交**

```bash
git add -A && git commit -m "docs: lesson 2.4 - memory system deep dive"
git push
```

---

### 任务 2.5：RAG 知识库 — 向量检索

**学习笔记输出：** `Learning/07-RAG知识库深度解析.md`

- [ ] **步骤：通读 `.claude/skills/ask-question/script/agent.py`**

理解 RAG 工作流：

```
用户提问 → 向量化提问 → Milvus 检索 → 获取 Top-K 相关文档 → LLM 生成回答
```

📝 **学习要点**：
- 什么是 Embedding？如何用 BGE 模型将文本变成向量？
- 什么是向量数据库？Milvus Lite 如何工作？
- Chunking（文档分块）的重要性
- 余弦相似度检索的原理

- [ ] **步骤：理解初始化脚本**

读 `.claude/skills/ask-question/script/init_knowledge_base.py`

```bash
python .claude/skills/ask-question/script/init_knowledge_base.py
```

- [ ] **步骤：运行 RAG Agent 测试**

```bash
python tests/test_rag_agent.py
```

- [ ] **步骤：撰写笔记并提交**

```bash
git add -A && git commit -m "docs: lesson 2.5 - RAG knowledge base"
git push
```

---

### 任务 2.6：Skill 插件体系

**学习笔记输出：** `Learning/08-Skill插件体系深度解析.md`

- [ ] **步骤：通读 `agents/lazy_agent_registry.py`**

理解插件化架构的核心：

```python
class LazyAgentRegistry:
    """
    懒加载 Agent 注册器
    
    核心机制：
    1. 启动时扫描 .claude/skills/ 目录下的所有插件
    2. 只加载元数据（不加载代码）
    3. 首次调用时才动态 import 并实例化
    4. 用完后可以卸载释放内存
    """
    
    def __getitem__(self, name):
        """首次访问时自动加载"""
        if name not in self._cache:
            self._load_agent(name)  # 动态 import
        return self._cache[name]
```

📝 **学习要点**：
- 插件架构的优势：可扩展性、解耦、独立开发
- 懒加载性能提升：启动 3 秒
- 对比 Java 的 SPI（Service Provider Interface）机制

- [ ] **步骤：阅读任意一个 Skill 的实现**

选一个 Skill（如 `preference/script/agent.py`），理解：
1. 它如何继承 `AgentBase`
2. 它如何实现 `reply()` 方法
3. 它如何与记忆系统交互

- [ ] **步骤：撰写笔记并提交**

```bash
git add -A && git commit -m "docs: lesson 2.6 - skill plugin architecture"
git push
```

---

### 任务 2.7：稳定性保障 — 熔断器与重试

**学习笔记输出：** `Learning/09-稳定性保障深度解析.md`

- [ ] **步骤：通读 `utils/circuit_breaker.py`**

理解状态机：

```
CLOSED (正常)
  → 连续失败 N 次 → OPEN (熔断)
    → 等待 T 秒 → HALF_OPEN (半开)
      → 成功 → CLOSED
      → 失败 → OPEN
```

- [ ] **步骤：通读 `utils/llm_resilience.py`**

理解指数退避重试：

```python
async def retry_with_backoff(func, max_retries=3, base_delay_sec=1.0):
    """指数退避重试"""
    for attempt in range(max_retries):
        try:
            return await func()
        except RetryableError:
            if attempt == max_retries - 1:
                raise
            delay = base_delay_sec * (2 ** attempt)  # 1s, 2s, 4s
            await asyncio.sleep(delay)
```

📝 **学习要点**：
- 熔断器是分布式系统的经典模式（Martin Fowler 论文）
- 指数退避如何防止「重试风暴」？
- 对比 Java 的 Resilience4j / Spring Retry

- [ ] **步骤：撰写笔记并提交**

```bash
git add -A && git commit -m "docs: lesson 2.7 - resilience mechanisms"
git push
```

---

## 阶段三：测试驱动的反刍与重构

### 任务 3.1：理解测试体系

**学习笔记输出：** `Learning/10-测试体系分析.md`

- [ ] **步骤：运行所有测试**

```bash
cd /home/ljh2923/pi-projects/项目学习/travel-Agent/repo
source venv/bin/activate
python tests/test_memory_system.py
python tests/test_intention_agent.py
python tests/test_orchestration.py
```

- [ ] **步骤：阅读测试代码的模式**

```python
# tests/test_memory_system.py 中的典型测试
def test_short_term_memory():
    """测试短期记忆的基本功能"""
    memory = ShortTermMemory(max_turns=2)
    
    # 添加消息
    memory.add_message("user", "你好")
    memory.add_message("assistant", "你好！有什么可以帮您？")
    
    # 验证
    context = memory.get_recent_context(2)
    assert len(context) == 2
```

📝 **学习要点**：
- Python 的 `assert` 测试方式 vs Java 的 JUnit
- 测试覆盖率映射到功能模块

- [ ] **步骤：撰写笔记并提交**

```bash
git add -A && git commit -m "docs: lesson 3.1 - test system analysis"
git push
```

---

### 任务 3.2-3.4：动手改造练习（三选一或全做）

#### 3.2：添加新的意图类型（Python）

**输出：** `Learning/11-动手改造-新增意图.md`

- [ ] **步骤：在 `intention_agent.py` 中添加新意图**

新增意图：「酒店预订（hotel_booking）」
1. 修改 Prompt，加入新意图的描述
2. 在 `lazy_agent_registry` 中注册对应 Skill
3. 编写测试用例

- [ ] **步骤：提交**

```bash
git add -A && git commit -m "feat: add hotel_booking intent"
git push
```

#### 3.3：用 SQLite 替换 JSON 存储（Python）

**输出：** `Learning/12-动手改造-SQLite存储.md`

- [ ] **步骤：改写 `long_term_memory.py`**

将 JSON 文件读写改为 SQLite 数据库读写

```python
# 核心改动
import sqlite3

class LongTermMemory:
    def __init__(self, user_id, storage_path):
        self.conn = sqlite3.connect(f"{storage_path}/memory.db")
        self._init_db()
    
    def _init_db(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS preferences (
                user_id TEXT, key TEXT, value TEXT
            )
        """)
```

#### 3.4：用 TypeScript 实现意图识别模块

**输出：** `Learning/13-三语扩展-TypeScript意图识别.md`

- [ ] **步骤：用 TypeScript 改写意图识别逻辑**

```typescript
// typescript/intention_agent.ts
interface Msg {
  name: string;
  content: string;
  role: 'user' | 'assistant' | 'system';
}

interface IntentionResult {
  intentions: string[];
  reasoning: string;
  rewrittenQuery: string;
  schedule: Record<string, string[]>;
}

class IntentionAgent {
  private model: string;
  
  constructor(modelName: string) {
    this.model = modelName;
  }
  
  async reply(input: Msg | Msg[]): Promise<IntentionResult> {
    // TypeScript 版实现
  }
}
```

---

## 阶段四：独立构建 AI Agent 项目

### 任务 4.1：选择项目

**输出：** `Learning/14-独立项目-设计文档.md`

从以下项目中选择一个：

| 项目 | 推荐语言 | 难度 |
|------|---------|:----:|
| 📝 **个人知识库问答助手** | Python | ⭐⭐ |
| 📅 **智能日程管理 Agent** | TypeScript | ⭐⭐⭐ |
| 🛒 **电商客服 Agent** | Java（Spring AI） | ⭐⭐⭐⭐ |

- [ ] **步骤：写 PRD（产品需求文档）**
- [ ] **步骤：设计架构图**
- [ ] **步骤：列出技术选型**

### 任务 4.2-4.N：迭代实现

- [ ] **步骤：实现意图识别模块**
- [ ] **步骤：实现记忆系统**
- [ ] **步骤：实现核心业务逻辑**
- [ ] **步骤：编写测试**
- [ ] **步骤：撰写总结笔记**

---

## 附录：三语对比速查表

| 概念 | Python | Java | TypeScript |
|------|--------|------|------------|
| 变量声明 | `name: str = "A"` | `String name = "A";` | `let name: string = "A"` |
| 列表/数组 | `list[str]` | `List<String>` | `string[]` |
| 字典/Map | `dict[str, any]` | `Map<String, Object>` | `Map<string, any>` |
| 类继承 | `class A(B)` | `class A extends B` | `class A extends B` |
| 接口 | 无关键词（鸭子类型） | `interface` | `interface` |
| 异步 | `async/await` | `CompletableFuture` | `async/await` |
| 并发执行 | `asyncio.gather()` | `CompletableFuture.allOf()` | `Promise.all()` |
| 异常处理 | `try/except` | `try/catch` | `try/catch` |
| 包管理 | pip | Maven/Gradle | npm |
| 类型系统 | 动态 + 注解(可选) | 静态强类型 | 静态 + 类型推断 |

---

## 学习进度跟踪表

```
第1阶段 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ✅
[x] 任务 1.1：确认开发环境          ⏱ 30分钟
[x] 任务 1.2：Python 核心语法速通     ⏱ 2小时

第2阶段 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[x] 任务 2.1：入口分析 — cli.py      ⏱ 1.5小时
[ ] 任务 2.2：意图识别智能体          ⏱ 2小时
[ ] 任务 2.3：协调器智能体            ⏱ 1.5小时
[ ] 任务 2.4：记忆系统                ⏱ 2小时
[ ] 任务 2.5：RAG 知识库             ⏱ 2小时
[ ] 任务 2.6：Skill 插件体系         ⏱ 1.5小时
[ ] 任务 2.7：稳定性保障              ⏱ 1小时

第3阶段 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] 任务 3.1：理解测试体系            ⏱ 1小时
[ ] 任务 3.2：动手改造（新增意图）     ⏱ 2小时
[ ] 任务 3.3：SQLite 替换 JSON       ⏱ 2小时
[ ] 任务 3.4：TypeScript 改写        ⏱ 3小时

第4阶段 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] 任务 4.1：独立项目设计            ⏱ 2小时
[ ] 任务 4.2：独立项目实现            ⏱ 8小时+

总预估时长：约 30-40 小时（每天 2 小时可 3-4 周完成）
```
