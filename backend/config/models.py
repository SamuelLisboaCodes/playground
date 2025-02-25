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
    user_id: str
    name: str
    instructions: str
    model: str
    tools: List[str]
    tools_resources: dict
    threads: List[str]

class User(BaseModel):
    id: str
    email: str
    token: str
    created_at: datetime
    assistants: List[str]