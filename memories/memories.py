from datetime import datetime
from typing import List, Optional, Dict, Any
from .mongodb_memories import MongoDBMemory, Message, Conversation


class MemoryManager:
    def __init__(self, connection_string: str = "mongodb://localhost:27017/"):
        self.db = MongoDBMemory(connection_string)

    def save_message(self, user_id: str, thread_id: str, role: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Add a message to the conversation."""
        return self.db.add_message(user_id, thread_id, role, content, metadata)

    def get_conversation_messages(self, user_id: str, thread_id: str, limit: Optional[int] = None) -> List[Message]:
        """Get messages from a specific conversation."""
        return self.db.get_conversation_messages(user_id, thread_id, limit)

    def get_conversation(self, user_id: str, thread_id: str) -> Optional[Conversation]:
        """Get the full conversation object."""
        return self.db.get_conversation(user_id, thread_id)

    def get_user_conversations(self, user_id: str, limit: int = 10) -> List[Conversation]:
        """Get all conversations for a user."""
        return self.db.get_user_conversations(user_id, limit)

    def delete_conversation(self, user_id: str, thread_id: str) -> bool:
        """Delete a specific conversation."""
        return self.db.delete_conversation(user_id, thread_id)

    def clear_user_conversations(self, user_id: str) -> bool:
        """Clear all conversations for a user."""
        return self.db.clear_user_conversations(user_id)

    def clear_all_conversations(self) -> bool:
        """Clear all conversations from the database."""
        return self.db.clear_all_conversations()

    def migrate_legacy_data(self) -> bool:
        """Migrate legacy data to new conversation format."""
        return self.db.migrate_legacy_data()

    # Backward compatibility methods
    def save_memory(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Legacy method - requires user_id and thread_id in metadata."""
        if not metadata or 'user_id' not in metadata or 'thread_id' not in metadata:
            raise ValueError("user_id and thread_id must be provided in metadata")
        
        user_id = metadata.pop('user_id')
        thread_id = metadata.pop('thread_id')
        return self.save_message(user_id, thread_id, role, content, metadata)

    def get_conversation_history(self, limit: int = 50, user_id: Optional[str] = None, thread_id: Optional[str] = None) -> List[Message]:
        """Get conversation history - requires user_id and thread_id."""
        if not user_id or not thread_id:
            raise ValueError("user_id and thread_id are required")
        return self.get_conversation_messages(user_id, thread_id, limit)

    def get_messages_by_role(self, user_id: str, thread_id: str, role: str, limit: Optional[int] = None) -> List[Message]:
        """Get messages by role from a conversation."""
        messages = self.get_conversation_messages(user_id, thread_id)
        filtered_messages = [msg for msg in messages if msg.role == role]
        if limit:
            return filtered_messages[-limit:]
        return filtered_messages

    def get_user_messages(self, user_id: str, thread_id: str, limit: Optional[int] = None) -> List[Message]:
        """Get all user messages from a conversation."""
        return self.get_messages_by_role(user_id, thread_id, 'user', limit)

    def get_assistant_messages(self, user_id: str, thread_id: str, limit: Optional[int] = None) -> List[Message]:
        """Get all assistant messages from a conversation."""
        return self.get_messages_by_role(user_id, thread_id, 'assistant', limit)

    def get_system_messages(self, user_id: str, thread_id: str, limit: Optional[int] = None) -> List[Message]:
        """Get all system messages from a conversation."""
        return self.get_messages_by_role(user_id, thread_id, 'system', limit)
