from openai import OpenAI 
from typing_extensions import override
from fastapi import APIRouter, Body, HTTPException
from config.models import  Assistant
import os

from dotenv import load_dotenv
from api.storage import users_collection, assistants_collection


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key= OPENAI_API_KEY)

router = APIRouter()

@router.post("/assistants", response_model=Assistant)
async def create_assistant(request: Assistant, email: str =  Body(..., embed=True)):
    """Cria um novo assistente na API da OpenAI"""
    print(request)
    assistant = client.beta.assistants.create(
        name=request.name,
        instructions=request.instructions,
        model=request.model,
        temperature=request.temperature,
        top_p=request.top_p
    )
    await assistants_collection.create_assistant(assistant)
    await users_collection.add_assistant_to_user(email, assistant.id)
    return Assistant(
        id=assistant.id,
        name=assistant.name,
        instructions=assistant.instructions,
        model=assistant.model,
        temperature=assistant.temperature,
        top_p=assistant.top_p
    )

@router.get("/assistants")
async def list_assistants(email: str):
    """Lista todos os assistentes criados"""
    assistants = client.beta.assistants.list()
    return [{"id": a.id, "name": a.name, "model": a.model} for a in assistants.data]

@router.get("/assistants/{assistant_id}/retrieve", response_model=Assistant)
async def retrieve_assistant(assistant_id: str):
    """Lista os atributos de um assistente pelo ID"""
    try:
        # Se for uma requisição assíncrona, precisa de await
        assistant_info =  client.beta.assistants.retrieve(assistant_id)

        return Assistant(
            id=assistant_info.id,
            name=assistant_info.name,
            instructions=assistant_info.instructions,
            model=assistant_info.model,
            temperature=assistant_info.temperature,
            max_tokens=0,
            top_p=assistant_info.top_p
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar assistente: {str(e)}")


@router.post("/assistants/{assistant_id}/update")
async def update_assistant(assistant_id: str, instructions: str, temperature: float, top_p:float, model: str ):
    update_assistant = client.beta.assistants.update(assistant_id = assistant_id,
                                     instructions = instructions,
                                     model=model, 
                                     temperature= temperature,
                                     top_p = top_p)
    return update_assistant