# 📚 第2课：Python 核心语法速通（面向 Java 开发者）

> **学习日期**：2026-05-25
> **学习目标**：面向 Java 开发者，快速掌握本项目用到的 Python 核心语法

---

## 一、开篇：Python vs Java 哲学 🎯

| 维度 | Java | Python |
|:----|:----|:-------|
| 📝 类型系统 | 静态强类型 | 动态类型 + 可选注解 |
| 🏗️ 代码结构 | 一切皆 class | 模块化，函数/类皆可顶层定义 |
| ⚡ 异步模型 | `CompletableFuture` | `async/await` + `asyncio` |
| 🔧 包管理 | Maven/Gradle | pip |
| 📂 文件组织 | 一个文件一个类 | 一个文件一个模块 |
| 🧪 测试 | JUnit | pytest / assert |

> 💡 **核心思维转变**：Java 是「严谨的建筑师」，Python 是「灵活的工匠」。本项目大量用 Python 的灵活特性来快速构建 AI Agent。

---

## 二、变量与类型 🔤

### 2.1 基础类型对比

```python
# ===== Java =====
# String name = "张三";
# int age = 25;
# double price = 99.9;
# boolean flag = true;
# List<String> list = new ArrayList<>();
# Map<String, Object> map = new HashMap<>();

# ===== Python =====
"""
变量声明——无需类型，Python 自动推断
"""
name: str = "张三"     # str（字符串）
age: int = 25          # int（整数，不限长度！）
price: float = 99.9    # float（浮点数）
flag: bool = True      # bool（布尔值，首字母大写！）
items: list[str] = ["北京", "上海", "杭州"]  # list（列表）
data: dict[str, any] = {"出发地": "北京", "时间": "2026-03-11"}  # dict（字典）
```

**📝 关键差异：**

| 概念 | Java | Python |
|:----|:----|:-------|
| 字符串 | `String` | `str`（小写） |
| 整数 | `int`（32位） | `int`（任意精度） |
| 浮点 | `double` | `float` |
| 布尔 | `boolean` | `bool`（`True`/`False` 首字母大写！） |
| 数组/列表 | `List<T>`（需 import） | `list`（内置类型，无需 import） |
| 键值对 | `Map<K,V>`（需 import） | `dict`（内置类型，无需 import） |
| 空值 | `null` | `None` |

### 2.2 字符串操作（本项目高频使用）

```python
# ---- f-string（最常用！⭐）----
name = "张三"
age = 25
# Java: String msg = "我叫" + name + "，今年" + age + "岁";
# Python:
msg = f"我叫{name}，今年{age}岁"
print(msg)  # 输出：我叫张三，今年25岁

# ---- 本项目实际使用 ----
user_input = "我想去北京出差"
context_str = f"""
【用户信息】
用户ID: {user_id}
当前时间: {current_time}

【用户输入】
{user_input}
"""
```

### 2.3 `list` 和 `dict`（核心数据结构）

```python
# ---- list（列表）----
cities: list[str] = ["北京", "上海", "杭州"]

# 增删改查
cities.append("深圳")           # 追加 → ["北京", "上海", "杭州", "深圳"]
cities.insert(1, "广州")       # 插入 → ["北京", "广州", "上海", "杭州", "深圳"]
cities.remove("上海")           # 删除元素
popped = cities.pop()           # 弹出末尾 → "深圳"
first = cities[0]               # 索引访问 → "北京"
exists = "北京" in cities        # 是否包含 → True
length = len(cities)            # 长度
sliced = cities[1:3]            # 切片 [1,3) → ["广州", "上海"]

# ---- dict（字典）----
person: dict[str, any] = {
    "name": "张三",
    "age": 25,
    "hobbies": ["编程", "旅行"],
}

# 增删改查
person["city"] = "北京"         # 新增键值对
person["age"] = 26              # 修改已有键
city = person.get("city", "未知")  # 安全获取（默认值）
keys = person.keys()            # 所有键
values = person.values()        # 所有值
exists = "name" in person       # 是否包含键 → True
del person["hobbies"]           # 删除键

# ---- 本项目实际使用 ----
intention_result = {
    "intentions": ["itinerary_planning", "event_collection"],
    "reasoning": "用户想要规划行程...",
    "schedule": {
        "priority_1": ["event_collection", "preference"],
        "priority_2": ["itinerary_planning"],
    },
}
# 访问嵌套数据
first_intent = intention_result["intentions"][0]    # → "itinerary_planning"
priority_1 = intention_result["schedule"]["priority_1"]  # → ["event_collection", "preference"]
```

---

## 三、函数定义与类型注解 🎯

### 3.1 基础函数

```python
# ===== Java =====
# public String greet(String name) {
#     return "Hello " + name;
# }

# ===== Python =====
def greet(name: str) -> str:
    """
    打招呼函数
    
    Args:
        name: 用户名
    
    Returns:
        问候语字符串
    """
    return f"Hello {name}"
```

**📝 关键差异：**

| 特性 | Java | Python |
|:----|:----|:-------|
| 定义 | `public Xxx method()` | `def method():` |
| 访问修饰符 | `public/private/protected` | 没有！（一切公开） |
| 返回类型 | 写在方法名前 | `-> str` 写在参数后 |
| 方法体 | 必须用 `{}` | 用缩进（通常4空格） |
| 文档注释 | `/** ... */` | `"""docstring"""` |

### 3.2 默认参数与关键字参数（Java 没有！）

```python
"""
默认参数——Java 需要重载，Python 一行解决
"""
def process_query(user_input: str, max_tokens: int = 8192, temperature: float = 0.7) -> dict:
    """
    处理用户查询
    
    Args:
        user_input: 用户输入
        max_tokens: 最大token数（默认8192）
        temperature: 温度参数（默认0.7）
    
    Returns:
        处理结果字典
    """
    return {
        "query": user_input,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

# 调用方式多样
process_query("你好")                                    # 只用必选参数
process_query("你好", max_tokens=4096)                    # 指定某个可选参数
process_query("你好", temperature=0.9, max_tokens=4096)   # 乱序指定（关键字参数）
```

### 3.3 `*args` 和 `**kwargs`（可变参数）

```python
"""
可变参数——Java 用 ... 或重载，Python 用 *args/**kwargs
"""
# *args = 任意数量的位置参数 → 元组
def log_messages(*messages: str) -> None:
    """记录多条消息"""
    for msg in messages:
        print(f"[LOG] {msg}")

log_messages("开始", "处理中", "完成")

# **kwargs = 任意数量的关键字参数 → 字典
def configure(**settings: any) -> None:
    """配置系统参数"""
    for key, value in settings.items():
        print(f"设置 {key} = {value}")

configure(llm_model="gpt-4", temperature=0.7, max_tokens=8192)

# 本项目实际使用（Agent 的 reply 方法）
async def reply(self, x: Optional[Union[Msg, List[Msg]]] = None, **kwargs) -> Msg:
    """
    统一的 Agent 回复接口
    
    Args:
        x: 输入消息
        **kwargs: 额外参数（扩展用）
    """
    pass
```

---

## 四、类与继承 🏗️

### 4.1 基础类定义

```python
# ===== Java =====
# public class User {
#     private String name;
#     
#     public User(String name) {
#         this.name = name;
#     }
#     
#     public String getName() {
#         return name;
#     }
# }

# ===== Python =====
class User:
    """
    用户类——对比 Java 的 POJO
    
    说明：Python 没有 private/public 关键字，
    靠命名约定：_前缀=保护，__前缀=私有
    """
    
    def __init__(self, name: str, age: int):
        """
        构造方法（相当于 Java 的构造器）
        
        Args:
            name: 用户名
            age: 年龄
        """
        self.name = name        # 公开属性
        self._age = age         # "保护"属性（约定，不强制）
        self.__secret = "隐藏"   # "私有"属性（name mangling）
    
    def greet(self) -> str:
        """实例方法（相当于 Java 的普通方法）"""
        return f"你好，我是{self.name}"
```

### 4.2 继承——本项目的核心模式 ⭐

```python
# ===== Java =====
# public class IntentionAgent extends AgentBase {
#     @Override
#     public Msg reply(Msg x) { ... }
# }

# ===== Python =====
class AgentBase:
    """Agent 基类——定义所有 Agent 的统一接口"""
    
    def __init__(self, name: str):
        self.name = name
        self.memory: list = []
    
    async def reply(self, x: any) -> any:
        """基类默认实现（可被子类覆盖）"""
        raise NotImplementedError("子类必须实现此方法")


class IntentionAgent(AgentBase):
    """
    意图识别智能体——继承 AgentBase
    
    对比 Java：class IntentionAgent extends AgentBase
    """
    
    def __init__(self, name: str, model: str = "gpt-4", **kwargs):
        """
        构造器
        
        Args:
            name: Agent 名称
            model: 使用的模型名
            **kwargs: 其他参数（传递给父类）
        """
        # 调用父类构造器（相当于 Java 的 super()）
        super().__init__(name)
        self.model = model
    
    async def reply(self, x: any) -> any:
        """
        覆盖父类的 reply 方法（相当于 Java 的 @Override）
        
        Args:
            x: 输入消息
        
        Returns:
            输出消息
        """
        # 处理逻辑...
        result = {"intent": "itinerary_planning"}
        return result
```

**📝 继承要点对比：**

| 特性 | Java | Python |
|:----|:----|:-------|
| 继承 | `class A extends B` | `class A(B)` |
| 调用父类构造器 | `super(x, y)` | `super().__init__(x, y)` |
| 方法重写 | `@Override` | 直接重写（无注解） |
| 抽象方法 | `abstract` 关键字 | `raise NotImplementedError` |
| 多继承 | ❌ 不支持（接口除外） | ✅ 支持 `class A(B, C)` |

### 4.3 本项目实际类结构

```
AgentBase (基类)
    ├── IntentionAgent          # 意图识别（预加载）
    ├── OrchestrationAgent      # 协调器（预加载）
    └── SkillAgent (各子 Agent)  # 通过 LazyAgentRegistry 懒加载
        ├── MemoryQueryAgent
        ├── PreferenceAgent
        ├── PlanTripAgent
        ├── InformationQueryAgent
        ├── RAGKnowledgeAgent
        └── EventCollectionAgent
```

---

## 五、async/await 异步编程 ⭐ **最核心！**

> 这是本项目用得最多的特性，必须掌握！

### 5.1 从同步到异步

```python
# ===== 同步版本（像 Java 的普通方法）=====
def fetch_weather_sync(city: str) -> str:
    """同步获取天气——会阻塞等待"""
    import time
    time.sleep(1)  # 模拟网络请求，阻塞！
    return f"{city}: 25°C"

# ===== 异步版本（相当于 Java 的 CompletableFuture）=====
import asyncio

async def fetch_weather_async(city: str) -> str:
    """
    异步获取天气——不会阻塞
    
    async def = 定义异步函数
    对比 Java：CompletableFuture<String> fetchWeather(String city)
    """
    await asyncio.sleep(1)  # await = 让出控制权，不阻塞
    return f"{city}: 25°C"
```

### 5.2 并发执行——本项目的灵魂 🔥

```python
# ===== Java =====
# CompletableFuture.allOf(
#     fetchWeather("北京"),
#     fetchWeather("上海"),
#     fetchWeather("杭州")
# ).join();

# ===== Python =====
async def main():
    """
    并发获取多个城市的天气
    
    对比 Java：CompletableFuture.allOf() 的并行效果
    """
    cities = ["北京", "上海", "杭州"]
    
    # asyncio.gather() = 并发执行多个异步任务
    # 对比 Java：CompletableFuture.allOf()
    results = await asyncio.gather(
        fetch_weather_async("北京"),
        fetch_weather_async("上海"),
        fetch_weather_async("杭州"),
    )
    print(results)  # ['北京: 25°C', '上海: 26°C', '杭州: 23°C']

# 启动事件循环
# 对比 Java：CompletableFuture 不需要显式启动
asyncio.run(main())
```

### 5.3 本项目实际使用：OrchestrationAgent 的并行调度

```python
# orchestration_agent.py 中的核心调度逻辑（简化版）
class OrchestrationAgent(AgentBase):
    """协调器——按优先级并行调度子 Agent"""
    
    async def _execute_agents(self, agents_to_run: list, context: str) -> list:
        """
        按优先级执行智能体
        
        核心逻辑：
        1. 按优先级分组
        2. 同优先级的 Agent 并行执行（asyncio.gather）
        3. 不同优先级串行执行
        """
        # 按优先级分组
        priority_groups = {}
        for item in agents_to_run:
            priority = item.get("priority", 1)
            priority_groups.setdefault(priority, []).append(item)
        
        # 从高优先级到低优先级依次执行
        for priority in sorted(priority_groups.keys()):
            group = priority_groups[priority]
            
            if len(group) == 1:
                # 单个 Agent：直接执行
                result = await self._run_single_agent(group[0], context)
            else:
                # 多个 Agent：并行执行！⭐
                tasks = [
                    self._run_single_agent(item, context) 
                    for item in group
                ]
                # 关键代码：asyncio.gather 并发执行
                parallel_results = await asyncio.gather(*tasks)
```

### 5.4 三语对比

| 操作 | Python | Java | TypeScript |
|:----|:------|:----|:----------|
| 定义异步函数 | `async def fn()` | `CompletableFuture<T>` | `async function fn()` |
| 等待结果 | `await fn()` | `fn().get()` | `await fn()` |
| 并发执行 | `asyncio.gather(a(), b())` | `CompletableFuture.allOf(a, b)` | `Promise.all([a(), b()])` |
| 事件循环 | `asyncio.run(main())` | `CompletableFuture` 自动管理 | `await` 自动管理 |

---

## 六、异常处理 🛡️

```python
# ===== Java =====
# try {
#     result = agent.reply(input);
# } catch (JSONException e) {
#     log.error("JSON解析失败", e);
# } catch (Exception e) {
#     log.error("未知错误", e);
# } finally {
#     cleanup();
# }

# ===== Python =====
import json

async def process_safely(user_input: str) -> dict:
    """
    安全的处理函数
    
    对比 Java 的 try-catch-finally
    """
    try:
        # 可能抛出异常的代码
        result = await call_llm(user_input)
        parsed = json.loads(result)
        return parsed
    
    except json.JSONDecodeError as e:
        """
        捕获特定异常
        
        对比 Java：catch (JSONException e)
        """
        print(f"❌ JSON 解析失败: {e}")
        return {"error": "parse_error", "fallback": user_input}
    
    except TimeoutError:
        """
        捕获超时异常
        """
        print(f"⏱️ 请求超时")
        return {"error": "timeout"}
    
    except Exception as e:
        """
        捕获所有异常（兜底）
        
        对比 Java：catch (Exception e)
        """
        print(f"❌ 未知错误: {type(e).__name__}: {e}")
        return {"error": "unknown"}
    
    finally:
        """
        无论是否异常都会执行
        
        对比 Java：finally { cleanup(); }
        """
        print("🧹 清理资源...")
```

**📝 异常处理对比：**

| 特性 | Java | Python |
|:----|:----|:-------|
| 基础结构 | `try-catch-finally` | `try-except-finally` |
| 捕获特定异常 | `catch (XxxException e)` | `except XxxException as e` |
| 捕获所有异常 | `catch (Exception e)` | `except Exception as e` |
| 抛出异常 | `throw new XxxException()` | `raise XxxException()` |
| 自定义异常 | `class MyEx extends Exception` | `class MyEx(Exception)` |
| 受检异常 | ✅ 编译时检查 | ❌ 没有受检异常 |

---

## 七、动手练习 🧪

### 练习1：把之前的 simple_intention.py 改写成异步版本

你已经写过了 `simple_intention.py`，这次我们给它加一个**三语对比**功能，输出 Python / Java / TypeScript 的语法对照：

```python
# learning_challenges/syntax_comparison.py
"""
三语语法对照练习
对比 Python / Java / TypeScript 的常见语法差异
"""

# 任务1：用 f-string 实现变量插值（对比 Java 的 + 拼接）
# Java:  String msg = "Hello, " + name + "!";
# Python: 请使用 f-string 实现
name = "张三"
# ✏️ 在下面写出 Python 的 f-string 版本
msg = ...


# 任务2：用 dict 替代 Java 的 HashMap
# Java:  Map<String, Object> user = new HashMap<>();
# Python: 请创建一个 dict
user = ...
# 添加键值对：name="张三", age=25, city="北京"


# 任务3：用 asyncio.gather 替代 Java 的 CompletableFuture.allOf
# 请用 async/await 实现并行获取3个城市的天气
import asyncio

async def get_weather(city: str) -> str:
    """模拟获取天气"""
    await asyncio.sleep(1)
    return f"{city}: 25°C"

async def main():
    """
    使用 asyncio.gather 并发执行
    """
    # ✏️ 在这里实现并行获取北京、上海、杭州的天气
    ...

if __name__ == "__main__":
    asyncio.run(main())


# 练习4（挑战）：class 继承
# 对比 Java 的 class IntentionAgent extends AgentBase
# 请创建一个继承体系
class AgentBase:
    """Agent 基类"""
    
    async def reply(self, input_data: str) -> str:
        """回复方法（抽象）"""
        raise NotImplementedError


class MyIntentionAgent(AgentBase):
    """你的意图识别 Agent"""
    
    def __init__(self, name: str):
        self.name = name
    
    async def reply(self, input_data: str) -> str:
        # ✏️ 实现：根据关键词返回意图
        # 如果输入包含"去"或"规划"，返回"行程规划"
        # 如果输入包含"天气"，返回"信息查询"
        # 否则返回"其他"
        ...
```

---

## 八、总结 📖

### 快速记忆卡片

| Java 概念 | Python 写法 | 备注 |
|:---------|:----------|:----|
| `String s = "x"` | `s: str = "x"` | 类型注解可选 |
| `List<T>` | `list[T]` | 内置，无需 import |
| `Map<K,V>` | `dict[K,V]` | 内置，无需 import |
| `null` | `None` | 大写 N！|
| `&& \|\| !` | `and or not` | 英文单词！|
| `true/false` | `True/False` | **首字母大写！** |
| `if (x > 0) {}` | `if x > 0:` | 无括号，有冒号+缩进 |
| `for (int i=0; i<n; i++)` | `for i in range(n):` | Pythonic |
| `for (String s : list)` | `for s in list:` | 简洁 |
| `try-catch-finally` | `try-except-finally` | 注意拼写 |
| `// 注释` | `# 注释` | 井号 |
| `/* ... */` | `"""..."""` | 文档字符串 |

### ⚠️ 最容易犯的错（特别提醒）

```python
# 错误1：布尔值小写了
flag = true   # ❌ NameError: name 'true' is not defined
flag = True   # ✅ 首字母大写

# 错误2：用了 && || !
if x > 0 && y < 10:  # ❌ SyntaxError
if x > 0 and y < 10: # ✅ 用 and/or/not

# 错误3：忘记冒号
if x > 0      # ❌ SyntaxError: expected ':'
if x > 0:     # ✅

# 错误4：漏了 self
class User:
    def greet(name):  # ❌ 少一个参数
        return f"你好，{name}"
    def greet(self, name):  # ✅ 第一个参数必须是 self
        return f"你好，{name}"

# 错误5：可变默认参数陷阱
def add_item(item, items=[]):  # ❌ 默认列表会共享！
    items.append(item)
    return items

def add_item(item, items=None):  # ✅ 用 None 代替
    if items is None:
        items = []
    items.append(item)
    return items
```

---

## ✅ 课后任务

- [ ] 完成上面的**练习1**（三语对照填空）
- [ ] 在本地运行已写好的 `simple_intention.py` 和 `simple_memory.py`，体会 Python 语法
- [ ] 把这节课提到的每个语法点在 `venv` 里实际跑一遍
- [ ] 提交代码：`git add -A && git commit -m "docs: lesson 2 - Python syntax crash course"`

---

> **📌 下节课预告**：第3课「CLI 入口分析 —— cli.py」—— 我们将深入 Aligo 项目的入口文件，追踪从用户输入到 Agent 响应的完整请求链路。
