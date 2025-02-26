from openai import OpenAI 
from typing_extensions import override
from fastapi import APIRouter
from config.models import  Assistant
from api.storage import users_collection, assistants_collection
client = OpenAI(api_key= 'OPENAI_API_KEY')

router = APIRouter()

@router.post("/assistants", response_model=Assistant)
async def create_assistant(request: Assistant):
    """Cria um novo assistente na API da OpenAI"""
    assistant = client.beta.assistants.create(
        name=request.name,
        instructions=request.instructions,
        model=request.model,
        temperature=request.temperature,
        top_p=request.top_p
    )
    assistants_collection.create_assistant(Assistant, assistant.max_tokens)
    users_collection.add_assistant_to_user("rodrigoquaglio@gmail.com", assistant.id)
    return Assistant(
        id=assistant.id,
        name=assistant.name,
        instructions=assistant.instructions,
        model=assistant.model,
        temperature=assistant.temperature,
        max_tokens=request.max_tokens,
        top_p=assistant.top_p
    )

@router.get("/assistants")
async def list_assistants():
    """Lista todos os assistentes criados"""
    assistants = client.beta.assistants.list()
    return [{"id": a.id, "name": a.name, "model": a.model} for a in assistants.data]