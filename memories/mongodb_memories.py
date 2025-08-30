import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import json
from bson import ObjectId
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import ConnectionFailure, OperationFailure


@dataclass
class Message:
    """Represents a single message in a conversation."""
    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> dict:
        """Convert Message object to dictionary."""
        data = {k: v for k, v in asdict(self).items() if v is not None}
        return data


@dataclass
class Conversation:
    """Represents a complete conversation with multiple messages."""
    conversation_id: str  # Unique conversation identifier
    user_id: str
    thread_id: str
    messages: List[Message]
    created_at: datetime
    updated_at: datetime
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> dict:
        """Convert Conversation object to dictionary for MongoDB storage."""
        data = asdict(self)
        # Convert messages to dict format
        data['messages'] = [msg.to_dict() for msg in self.messages]
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Conversation":
        """Create Conversation object from dictionary."""
        # Convert message dicts back to Message objects
        messages = []
        for msg_data in data.get('messages', []):
            # Handle datetime conversion if needed
            if 'timestamp' in msg_data and isinstance(msg_data['timestamp'], str):
                msg_data['timestamp'] = datetime.fromisoformat(msg_data['timestamp'])
            messages.append(Message(**msg_data))
        
        # Handle datetime conversion for conversation timestamps
        if 'created_at' in data and isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if 'updated_at' in data and isinstance(data['updated_at'], str):
            data['updated_at'] = datetime.fromisoformat(data['updated_at'])
            
        return cls(
            conversation_id=data['conversation_id'],
            user_id=data['user_id'],
            thread_id=data['thread_id'],
            messages=messages,
            created_at=data['created_at'],
            updated_at=data['updated_at'],
            metadata=data.get('metadata')
        )


class MongoDBMemory:
    def __init__(self, connection_string: str = "mongodb://localhost:27017/"):
        self.client = MongoClient(connection_string)
        self.db = self.client.memories
        self.collection = self.db.conversations
        
        # Create indexes for better performance
        self._create_indexes()

    def _create_indexes(self):
        """Create indexes for better query performance."""
        try:
            # First, clean up any documents without conversation_id
            self._cleanup_legacy_data()
            
            # Index on user_id and thread_id for faster lookups
            self.collection.create_index([("user_id", 1), ("thread_id", 1)])
            # Index on conversation_id for unique lookups (only for non-null values)
            self.collection.create_index("conversation_id", unique=True, sparse=True)
            # Index on updated_at for recent conversations
            self.collection.create_index([("updated_at", -1)])
        except Exception as e:
            print(f"Warning: Could not create indexes: {e}")

    def _cleanup_legacy_data(self):
        """Clean up legacy data that doesn't fit the new structure."""
        try:
            # Remove documents that don't have conversation_id or have null conversation_id
            result = self.collection.delete_many({
                "$or": [
                    {"conversation_id": {"$exists": False}},
                    {"conversation_id": None}
                ]
            })
            if result.deleted_count > 0:
                print(f"Cleaned up {result.deleted_count} legacy documents")
        except Exception as e:
            print(f"Warning: Could not cleanup legacy data: {e}")

    def get_or_create_conversation(self, user_id: str, thread_id: str) -> Conversation:
        """Get existing conversation or create a new one."""
        conversation_doc = self.collection.find_one({
            "user_id": user_id,
            "thread_id": thread_id
        })
        
        if conversation_doc:
            conversation_doc.pop("_id", None)
            return Conversation.from_dict(conversation_doc)
        else:
            # Create new conversation
            conversation_id = f"{user_id}_{thread_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            new_conversation = Conversation(
                conversation_id=conversation_id,
                user_id=user_id,
                thread_id=thread_id,
                messages=[],
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            self.collection.insert_one(new_conversation.to_dict())
            return new_conversation

    def add_message(self, user_id: str, thread_id: str, role: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Add a message to the conversation."""
        conversation = self.get_or_create_conversation(user_id, thread_id)
        
        # Create new message
        new_message = Message(
            role=role,
            content=content,
            timestamp=datetime.now(),
            metadata=metadata
        )
        
        # Add message to conversation
        conversation.messages.append(new_message)
        conversation.updated_at = datetime.now()
        
        # Update in database
        self.collection.update_one(
            {"conversation_id": conversation.conversation_id},
            {
                "$set": {
                    "messages": [msg.to_dict() for msg in conversation.messages],
                    "updated_at": conversation.updated_at
                }
            }
        )
        
        return conversation.conversation_id

    def get_conversation(self, user_id: str, thread_id: str) -> Optional[Conversation]:
        """Get a specific conversation."""
        conversation_doc = self.collection.find_one({
            "user_id": user_id,
            "thread_id": thread_id
        })
        
        if conversation_doc:
            conversation_doc.pop("_id", None)
            return Conversation.from_dict(conversation_doc)
        return None

    def get_conversation_messages(self, user_id: str, thread_id: str, limit: Optional[int] = None) -> List[Message]:
        """Get messages from a conversation."""
        conversation = self.get_conversation(user_id, thread_id)
        if not conversation:
            return []
        
        messages = conversation.messages
        if limit:
            messages = messages[-limit:]  # Get last N messages
        return messages

    def get_user_conversations(self, user_id: str, limit: int = 10) -> List[Conversation]:
        """Get all conversations for a user."""
        cursor = self.collection.find({"user_id": user_id}).sort("updated_at", DESCENDING).limit(limit)
        conversations = []
        for doc in cursor:
            doc.pop("_id", None)
            conversations.append(Conversation.from_dict(doc))
        return conversations

    def delete_conversation(self, user_id: str, thread_id: str) -> bool:
        """Delete a specific conversation."""
        try:
            result = self.collection.delete_one({
                "user_id": user_id,
                "thread_id": thread_id
            })
            return result.deleted_count > 0
        except Exception:
            return False

    def clear_user_conversations(self, user_id: str) -> bool:
        """Clear all conversations for a user."""
        try:
            self.collection.delete_many({"user_id": user_id})
            return True
        except Exception:
            return False

    def get_conversation_by_id(self, conversation_id: str) -> Optional[Conversation]:
        """Get conversation by its unique ID."""
        conversation_doc = self.collection.find_one({"conversation_id": conversation_id})
        if conversation_doc:
            conversation_doc.pop("_id", None)
            return Conversation.from_dict(conversation_doc)
        return None

    def clear_all_conversations(self) -> bool:
        """Clear all conversations from the database."""
        try:
            self.collection.delete_many({})
            return True
        except Exception:
            return False

    def migrate_legacy_data(self) -> bool:
        """Migrate legacy individual message documents to conversation format."""
        try:
            # This method can be used to migrate old data if needed
            # For now, we'll just clean up incompatible documents
            self._cleanup_legacy_data()
            return True
        except Exception as e:
            print(f"Error during migration: {e}")
            return False
