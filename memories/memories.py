from datetime import datetime
from typing import List, Optional
from mongodb_memories import MongoDBMemory, Memory


class MemoryManager:
    def __init__(self, connection_string: str = "mongodb://localhost:27017/"):
        self.db = MongoDBMemory(connection_string)

    def save_memory(self, role: str, content: str, metadata: dict = None) -> str:
        """Save a new memory to MongoDB."""
        memory = Memory(
            role=role,
            content=content,
            timestamp=datetime.now(),
            metadata=metadata
        )
        return self.db.save_memory(memory)

    def fetch_memories(self, limit: int = 10) -> List[Memory]:
        """Fetch recent memories from MongoDB."""
        return self.db.collection.find().sort('timestamp', -1).limit(limit)

    def fetch_memories_by_role(self, role: str, limit: Optional[int] = None) -> List[Memory]:
        """Fetch memories by role from MongoDB."""
        query = {'role': role}
        cursor = self.db.collection.find(query).sort('timestamp', -1)
        if limit:
            cursor = cursor.limit(limit)
        return list(cursor)
