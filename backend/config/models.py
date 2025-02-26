from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

#Classe referente ao "run" do prompt
class Run(BaseModel):
    id: str
    thread_id: str
    assistant_id: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None

#classe referente a uma thread de cada assistant no playground
class Thread(BaseModel):
    id: str
    #messages vai receber a id de cada mensagem e colocado em uma lista para poder ser localizado mais facil
    messages: List[str] = []
    #messages vai receber a id de cada run e colocado em uma lista para poder ser localizado mais facil
    runs: List[str] = []

#Classe referente a mensagem enviada e uma thread
class Message(BaseModel):
    id: str
    thread_id: str
    assistant_id: Optional[str]
    role: str  
    content: str
    timestamp: datetime

#Classe referente ao assistant criado
class Assistant(BaseModel):
    id: str
    name: str
    instructions: str
    model: str
    tools: List[str] = []
    tools_resources: dict = []
    temperature: float
    max_tokens: int
    top_p: float


#Classe do usuario
class User(BaseModel):
    id: str
    email: str
    refresh_token: Optional[str]
    assistants: List[str] = []
    threads: List[str] = []