"""
三语语法对照练习
对比 Python / Java / TypeScript 的常见语法差异

使用方法：逐题完成填空，然后用 python 运行验证
"""
import asyncio


# ============================================================
# 任务1：f-string 变量插值
# ============================================================
"""
Java:  String msg = "Hello, " + name + "!";
TS:    const msg = `Hello, ${name}!`;
Python: f-string 实现
"""
def task1_fstring():
    """f-string 练习"""
    name = "张三"
    age = 25
    city = "北京"
    
    # ✏️ TODO: 使用 f-string 生成 "我叫张三，今年25岁，来自北京"
    msg = ...
    
    print(msg)
    return msg


# ============================================================
# 任务2：dict 替代 HashMap
# ============================================================
"""
Java:  Map<String, Object> user = new HashMap<>();
       user.put("name", "张三");
       user.put("age", 25);

Python: 直接用 dict 字面量
"""
def task2_dict():
    """dict 练习"""
    # ✏️ TODO: 创建一个 dict，包含 name, age, city 三个字段
    user = ...
    
    # ✏️ TODO: 添加一个键值对 hobbies: ["编程", "旅行"]
    ...
    
    # ✏️ TODO: 获取 age 的值（使用 get 方法，带默认值 0）
    age = ...
    
    print(f"用户: {user}")
    print(f"年龄: {age}")
    return user


# ============================================================
# 任务3：list 操作
# ============================================================
"""
Java:  List<String> cities = new ArrayList<>(Arrays.asList("北京", "上海"));
       cities.add("杭州");
       
Python: list 直接创建
"""
def task3_list():
    """list 练习"""
    # ✏️ TODO: 创建一个列表，包含 "北京", "上海", "杭州"
    cities = ...
    
    # ✏️ TODO: 追加 "深圳" 到列表
    ...
    
    # ✏️ TODO: 获取列表长度
    length = ...
    
    # ✏️ TODO: 判断 "上海" 是否在列表中
    has_shanghai = ...
    
    print(f"城市列表: {cities}")
    print(f"数量: {length}")
    print(f"有上海吗: {has_shanghai}")
    return cities


# ============================================================
# 任务4：函数定义 + 类型注解
# ============================================================
"""
Java:  public String greet(String name, int age) {
           return String.format("我叫%s，今年%d岁", name, age);
       }

Python: def 函数定义
"""
# ✏️ TODO: 定义一个函数 greet，参数 name: str, age: int，返回 str
def greet(...) -> ...:
    """打招呼函数"""
    ...


# ============================================================
# 任务5：类与继承
# ============================================================
"""
Java:  class IntentionAgent extends AgentBase {
           private String name;
           public IntentionAgent(String name) {
               super();
               this.name = name;
           }
           @Override
           public String reply(String input) { return "意图识别结果"; }
       }
"""

class AgentBase:
    """Agent 基类——定义统一接口"""
    
    async def reply(self, input_data: str) -> str:
        """
        回复方法（抽象方法）
        
        Args:
            input_data: 用户输入
        
        Returns:
            处理结果
        """
        raise NotImplementedError("子类必须实现此方法")


class MyIntentionAgent(AgentBase):
    """
    意图识别 Agent——继承 AgentBase
    
    对比 Java：class MyIntentionAgent extends AgentBase
    """
    
    def __init__(self, name: str):
        """
        构造器
        
        Args:
            name: Agent 名称
        """
        # ✏️ TODO: 调用父类构造器（对比 Java 的 super()）
        ...
        
        # ✏️ TODO: 保存 name 到 self.name
        ...
    
    async def reply(self, input_data: str) -> str:
        """
        覆盖父类的 reply 方法
        
        规则：
        - 输入包含 "去" 或 "规划" → 返回 "行程规划"
        - 输入包含 "天气" → 返回 "信息查询"
        - 输入包含 "喜欢" 或 "偏好" → 返回 "偏好管理"
        - 否则 → 返回 "其他"
        
        Args:
            input_data: 用户输入
        
        Returns:
            意图名称
        """
        # ✏️ TODO: 实现意图识别逻辑
        ...


# ============================================================
# 任务6：async/await 异步编程 ⭐
# ============================================================
"""
Java:  CompletableFuture<String> fetchWeather(String city) {
           return CompletableFuture.supplyAsync(() -> {
               sleep(1000);
               return city + ": 25°C";
           });
       }
       
       CompletableFuture.allOf(
           fetchWeather("北京"),
           fetchWeather("上海"),
           fetchWeather("杭州")
       ).join();

Python: async/await + asyncio.gather
"""

async def fetch_weather(city: str) -> str:
    """
    异步获取天气（模拟）
    
    Args:
        city: 城市名
    
    Returns:
        天气信息
    """
    # ✏️ TODO: 模拟网络延迟 1 秒（使用 await asyncio.sleep(1)）
    ...
    
    return f"{city}: 25°C"


async def task6_async():
    """
    并发获取多个城市天气
    
    使用 asyncio.gather 并发执行
    对比 Java：CompletableFuture.allOf()
    对比 TS：  Promise.all()
    """
    cities = ["北京", "上海", "杭州"]
    
    print("正在查询天气...")
    
    # ✏️ TODO: 使用 asyncio.gather 并发获取3个城市的天气
    results = ...
    
    print(f"结果: {results}")
    return results


# ============================================================
# 任务7（挑战）：异常处理
# ============================================================
"""
Java:  try {
           int result = Integer.parseInt(str);
       } catch (NumberFormatException e) {
           System.out.println("解析失败: " + e.getMessage());
       } catch (Exception e) {
           System.out.println("未知错误");
       } finally {
           cleanup();
       }
"""
def task7_exception():
    """异常处理练习"""
    inputs = ["42", "abc", "3.14", "你好"]
    
    for val in inputs:
        # ✏️ TODO: 尝试将 val 转为 int，捕获 ValueError
        # 如果成功 → 打印 "数字: {结果}"
        # 如果失败 → 打印 "无法转换: {val}"
        # 最后都要打印 "处理完成: {val}"
        ...


# ============================================================
# 主函数
# ============================================================
async def main():
    """运行所有任务"""
    print("=" * 50)
    print("  📝 Python 语法练习")
    print("=" * 50)
    
    print("\n📌 任务2: dict 练习")
    task2_dict()
    
    print("\n📌 任务6: 异步编程（最难！）")
    await task6_async()
    
    print("\n✅ 完成！如果看到报错，看看是哪个任务还没实现~")


if __name__ == "__main__":
    asyncio.run(main())
