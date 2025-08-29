from typing_extensions import TypedDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class State(TypedDict, total=False):
    """State for saving and loading"""
    messages: List[Dict[str, Any]]  # Changed from list[AnyMessage] to Dict format
    user_id: Optional[str]
    created_at: Optional[datetime]  # Made optional
    query: Optional[str]
    response: Optional[str]
    search_results: Optional[List[Dict[str, Any]]]
    timestamp: Optional[str]
    user_question: Optional[str]