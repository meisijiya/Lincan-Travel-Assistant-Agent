"""
简化版记忆管理器
动手实现，理解本项目的两层记忆架构

对比 Java：类似于 CacheManager + Repository 的组合
"""
import json
import os
import time


class SimpleShortTermMemory:
    """
    简化版短期记忆——滑动窗口机制
    
    对比 Java：类似于一个固定大小的 LinkedList / Circular Buffer
    
    职责：保存最近 N 轮对话，超出时丢弃最旧的
    """
    
    def __init__(self, max_turns: int = 3):
        self.messages: list[dict] = []
        self.max_turns = max_turns
    
    def add_message(self, role: str, content: str):
        """
        添加消息到短期记忆
        
        Args:
            role: 角色（user/assistant）
            content: 消息内容
        """
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": time.time(),
        })
        
        # 滑动窗口：超出 max_turns 轮对话时，丢弃最旧的
        # 注意：一轮对话 = 1条user + 1条assistant = 2条记录
        max_records = self.max_turns * 2
        if len(self.messages) > max_records:
            self.messages = self.messages[-max_records:]
        
        print(f"  📥 [短期记忆] 已存储 ({len(self.messages)}/{max_records} 条)")
    
    def get_context(self, n_turns: int = None) -> str:
        """
        获取格式化的上下文文本
        
        Args:
            n_turns: 取最近多少轮（默认取全部）
        
        Returns:
            格式化的对话上下文
        """
        if n_turns:
            records = self.messages[-(n_turns * 2):]
        else:
            records = self.messages
        
        lines = []
        for msg in records:
            role_cn = "用户" if msg["role"] == "user" else "助手"
            lines.append(f"{role_cn}: {msg['content']}")
        
        return "\n".join(lines)


class SimpleLongTermMemory:
    """
    简化版长期记忆——JSON 文件持久化
    
    对比 Java：类似于 JPA Repository + Entity
    
    职责：跨会话持久化用户偏好和行程历史
    """
    
    def __init__(self, filepath: str = "test_memory.json"):
        self.filepath = filepath
        self.data = self._load()
    
    def _load(self) -> dict:
        """从 JSON 文件加载数据"""
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "preferences": {},    # 用户偏好
            "trips": [],          # 行程历史
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
    
    def save(self):
        """保存到 JSON 文件"""
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        print(f"  💾 [长期记忆] 已保存到 {self.filepath}")
    
    def add_preference(self, key: str, value: str, append: bool = False):
        """
        添加用户偏好
        
        支持追加和覆盖两种模式！
        对比 Java：类似于 update 方法，但智能判断是 add 还是 set
        
        Args:
            key: 偏好类型（如 hotel_brands, seat_preference）
            value: 偏好值
            append: True=追加（"我还喜欢..."），False=覆盖（"我改成..."）
        """
        if append and key in self.data["preferences"]:
            # 追加模式：如果已有值，转成列表再追加
            existing = self.data["preferences"][key]
            if isinstance(existing, list):
                if value not in existing:  # 避免重复
                    existing.append(value)
            else:
                self.data["preferences"][key] = [existing, value]
            print(f"  ➕ [偏好] 追加 {key}: {value}")
        else:
            # 覆盖模式：直接覆盖
            self.data["preferences"][key] = value
            print(f"  ✏️  [偏好] 设置 {key}: {value}")
        
        self.save()
    
    def add_trip(self, start: str, end: str, date: str, purpose: str):
        """添加行程记录"""
        self.data["trips"].append({
            "start": start,
            "end": end,
            "date": date,
            "purpose": purpose,
        })
        print(f"  📅 [行程] 记录: {start} → {end} ({date})")
        self.save()
    
    def get_preferences_summary(self) -> str:
        """获取偏好摘要"""
        if not self.data["preferences"]:
            return "暂无偏好记录"
        lines = []
        for key, value in self.data["preferences"].items():
            lines.append(f"  • {key}: {value}")
        return "\n".join(lines)
    
    def cleanup(self):
        """清理测试文件"""
        if os.path.exists(self.filepath):
            os.remove(self.filepath)


class SimpleMemoryManager:
    """
    简化版记忆管理器——统一管理两层记忆
    
    对比 Java：Facade 模式，封装底层复杂性
    """
    
    def __init__(self, user_id: str, max_turns: int = 3):
        self.user_id = user_id
        self.short_term = SimpleShortTermMemory(max_turns=max_turns)
        self.long_term = SimpleLongTermMemory(f"memory_{user_id}.json")
    
    def add_message(self, role: str, content: str):
        """同时存入短期和长期记忆"""
        self.short_term.add_message(role, content)
        self.long_term.data.setdefault("chat_history", []).append({
            "role": role,
            "content": content,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        })
        self.long_term.save()
    
    def get_full_context(self) -> str:
        """合并两层记忆为完整上下文"""
        parts = []
        # 长期记忆：偏好
        prefs = self.long_term.get_preferences_summary()
        if prefs != "暂无偏好记录":
            parts.append("【用户偏好】")
            parts.append(prefs)
        
        # 短期记忆：最近对话
        recent = self.short_term.get_context(n_turns=2)
        if recent:
            parts.append("【最近对话】")
            parts.append(recent)
        
        return "\n".join(parts)
    
    def cleanup(self):
        """清理所有数据"""
        self.long_term.cleanup()


def test_memory_system():
    """
    测试记忆系统
    模拟一个完整的用户交互场景
    """
    print("=" * 60)
    print("  🧪  记忆系统测试")
    print("=" * 60)
    
    # 创建记忆管理器
    mgr = SimpleMemoryManager(user_id="test_user", max_turns=3)
    print(f"\n👤 用户: {mgr.user_id}")
    
    # 模拟一次对话
    print("\n--- 第1轮对话 ---")
    mgr.long_term.add_preference("hotel_brands", "汉庭")
    mgr.add_message("user", "我喜欢住汉庭")
    mgr.add_message("assistant", "好的，已记录您的偏好")
    
    print("\n--- 第2轮对话（追加偏好）---")
    mgr.long_term.add_preference("hotel_brands", "如家", append=True)
    mgr.add_message("user", "我还喜欢如家")
    mgr.add_message("assistant", "好的，已追加如家到偏好列表")
    
    print("\n--- 第3轮对话（添加行程）---")
    mgr.long_term.add_trip("北京", "上海", "2026-04-15", "商务会议")
    mgr.add_message("user", "我要去上海出差")
    mgr.add_message("assistant", "好的，已记录您的出差计划")
    
    # 查看完整上下文
    print("\n" + "=" * 60)
    print("  📋  完整上下文")
    print("=" * 60)
    print(mgr.get_full_context())
    
    # 清理
    mgr.cleanup()
    print(f"\n🧹 测试文件已清理")


if __name__ == "__main__":
    test_memory_system()
