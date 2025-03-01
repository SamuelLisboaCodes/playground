from openai import OpenAI 
from typing_extensions import override
from fastapi import APIRouter, HTTPException, Body, UploadFile, File
from config.models import  Assistant, RagUploadPoll, RagUserFiles, RagVectorStore
import os
import base64


from dotenv import load_dotenv
from api.storage import users_collection, assistants_collection, rag_collection


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key= OPENAI_API_KEY)

router = APIRouter()

@router.post("/assistants", response_model=Assistant)
async def create_assistant(request: Assistant, user_email: str = Body(..., embed=True)):
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
    await users_collection.add_assistant_to_user(user_email, assistant.id)
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
    # assistants = client.beta.assistants.list()
    # return [{"id": a.id, "name": a.name, "model": a.model} for a in assistants.data]    
    assistants_ids = await users_collection.get_user_assistants(email)
    return assistants_ids.assistants

@router.get("/assistants/{assistant_id}/retrieve", response_model=Assistant)
async def retrieve_assistant(assistant_id: str):
    """Lista os atributos de um assistente pelo ID"""
    try:
        # Se for uma requisição assíncrona, precisa de await
        assistant_info =  client.beta.assistants.retrieve( assistant_id)
        print(assistant_info)
        return Assistant(
            id=assistant_info.id,
            name=assistant_info.name,
            instructions=assistant_info.instructions,
            model=assistant_info.model,
            temperature=assistant_info.temperature,
            top_p=assistant_info.top_p
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar assistente: {str(e)}")


@router.post("/assistants/{assistant_id}/update")
async def update_assistant(assistant_id: str, instructions: str = Body(..., embed=True), temperature: float = Body(..., embed=True), top_p: float = Body(..., embed=True), model: str= Body(..., embed=True)):
    update_assistant = client.beta.assistants.update(assistant_id = assistant_id,
                                     instructions = instructions,
                                     model=model,
                                     temperature= temperature,
                                     top_p = top_p)
    await assistants_collection.update_assistant(update_assistant)
    return update_assistant

@router.post("/assistants/{assistant_id}/toggle_file_search")
async def update_assistant(assistant_id: str, tools):
    update_assistant = client.beta.assistants.update(assistant_id = assistant_id, tools = tools)
    
    return update_assistant

@router.post("/assistants/{assistant_id}/delete")
async def delete_assistant(assistant_id: str, user_email: str = Body(..., embed=True)): 
    delete_assistant = client.beta.assistants.delete(assistant_id=assistant_id)
    await users_collection.remove_assistant_from_user(user_email=user_email, assistant_id=assistant_id)
    await assistants_collection.delete_assistant(assistant_id=assistant_id)
    

    return delete_assistant


@router.get("files/{file_id}")
async def retrive_file(file_id: str):
    get_file = await rag_collection.get_user_file(file_id)
    return get_file


@router.post("/create/vector_store")
async def create_RAG(vector_store: RagVectorStore):
    vector_created = client.beta.vector_stores.create(name= vector_store.name, file_ids=vector_store.file_ids)
    new_vector= await rag_collection.create_vector_store(vector_created)
    return  new_vector

@router.post("/create/files")
async def create_RAG(files_store: UploadFile = File(...)):

    file_created =  client.files.create(
  file= open(files_store ,'rb'),  
  purpose="assistant"
)
    # new_file = await rag_collection.create_user_files(file_created)
    return file_created

@router.post("/delete/files/{file_id}")
async def create_RAG(file_id: str):
    file_created =  client.files.delete(file_id)
    new_file = await rag_collection.delete_user_files(file_id)
    
    return new_file

@router.post("/vector_store_files/poll")
async def create_and_poll(rag_to_upload: RagUploadPoll):
    file_uploaded = client.beta.vector_stores.files.create_and_poll(
  vector_store_id= rag_to_upload.vector_id,
  file_ids= rag_to_upload.files
)
    return file_uploaded.id
