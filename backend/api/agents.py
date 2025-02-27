from openai import OpenAI 
from typing_extensions import override
from fastapi import APIRouter, Request
from config.models import  Assistant
import os
from api.storage import users_collection, assistants_collection
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

router = APIRouter()

@router.post("/assistants", response_model=Assistant)
async def create_assistant(request: Assistant):
    """Cria um novo assistente na API da OpenAI"""
    print(request)
    assistant = client.beta.assistants.create(
        name=request.name,
        instructions=request.instructions,
        model=request.model,
        temperature=request.temperature,
        top_p=request.top_p
    )
    new_assistant = await assistants_collection.create_assistant(assistant)
    await users_collection.add_assistant_to_user("rodrigoquaglio@gmail.com", assistant.id)
    return new_assistant

@router.get("/assistants")
async def list_assistants(email: str):
    """Lista todos os assistentes criados"""
    #assistants = client.beta.assistants.list()
    assistants_id_list = await users_collection.get_user_assistants(email)
    
    return [ await assistants_collection.get_assistant(id) for id in assistants_id_list]