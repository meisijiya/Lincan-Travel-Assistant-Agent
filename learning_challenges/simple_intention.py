"""
简单的意图识别模拟器
用于理解本项目的意图识别核心概念

对比 Java：类似于一个基于关键字匹配的路由器
"""
import asyncio
import json

# 意图类别映射（对比 Java 的 enum）
INTENTIONS = {
    "plan": "行程规划",
    "query": "信息查询",
    "preference": "偏好管理",
    "knowledge": "知识问答",
    "memory": "记忆查询",
    "unknown": "未识别",
}


async def detect_intention(user_input: str) -> dict:
    """
    模拟 LLM 意图识别（实际项目中调用大模型）
    
    对比 Java：类似于 Controller 层的请求路由
    
    Args:
        user_input: 用户输入的自然语言
    
    Returns:
        包含意图类型和调度计划的字典
    """
    # 关键词映射（实际项目用 LLM 语义理解，更准确）
    keywords = {
        "plan": ["规划", "安排", "去", "出差", "旅程", "旅行", "从"],
        "query": ["查询", "天气", "怎么样", "多少钱", "信息"],
        "preference": ["喜欢", "偏好", "习惯", "爱住", "想住"],
        "knowledge": ["标准", "报销", "政策", "规定", "指南", "知识"],
        "memory": ["去过", "之前", "历史", "什么时候", "回忆"],
    }
    
    # 检测意图（模拟 LLM 推理过程）
    detected = []
    for intent, words in keywords.items():
        for word in words:
            if word in user_input:
                detected.append(intent)
                break  # 每类意图只匹配一次
    
    if not detected:
        detected = ["unknown"]
    
    # 构建调度计划（模拟 OrchestrationAgent 的调度逻辑）
    # 优先级1：可以并行执行的任务
    # 优先级2：依赖优先级1结果的任务
    schedule = {"priority_1": [], "priority_2": []}
    if "plan" in detected:
        schedule["priority_1"].extend(["event_collection", "preference", "memory_query"])
        schedule["priority_2"].append("itinerary_planning")
    if "query" in detected:
        schedule["priority_1"].append("information_query")
    if "knowledge" in detected:
        schedule["priority_1"].append("rag_knowledge")
    if "preference" in detected:
        schedule["priority_1"].append("preference")
    if "memory" in detected:
        schedule["priority_1"].append("memory_query")
    
    return {
        "intentions": detected,
        "intent_names": [INTENTIONS[i] for i in detected],
        "reasoning": f"根据输入『{user_input}』，检测到意图: {[INTENTIONS[i] for i in detected]}",
        "schedule": schedule,
    }


async def main():
    """主函数：测试不同的输入"""
    test_inputs = [
        "我想3月11日从北京去杭州出差一周",
        "明天天气怎么样",
        "我喜欢住汉庭酒店",
        "出差住宿标准是多少",
        "我去过哪些地方旅游",
        "你好啊",
    ]
    
    print("=" * 60)
    print("  🧠  意图识别模拟器   ")
    print("=" * 60)
    
    for inp in test_inputs:
        print(f"\n📝 用户输入: {inp}")
        result = await detect_intention(inp)
        print(f"🔍 识别结果: {result['intent_names']}")
        print(f"💭 推理过程: {result['reasoning']}")
        print(f"📋 调度计划: {result['schedule']}")
        print("-" * 60)


if __name__ == "__main__":
    asyncio.run(main())
