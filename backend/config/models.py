from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


class Run(BaseModel):
    id: str
    thread_id: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None

class Thread(BaseModel):
    id: str
    assistant_id: str
    messages: List[str]
    runs: List[str]

class Message(BaseModel):
    id: str
    thread_id: str
    role: str  
    content: str
    timestamp: datetime

class Assistant(BaseModel):
    id: str
    name: str
    instructions: str
    model: str
    temperature: float
    max_tokens: int
    top_p: float
    
class User(BaseModel):
    id: str
    email: EmailStr
    refresh_token: Optional[str]
    created_at: datetime
    assistants: List[str] = []