from fastapi import APIRouter, HTTPException, Body
from openai import OpenAI
from config.models import Thread, Message, Run
from datetime import datetime
from typing import List
from dotenv import load_dotenv
import time
import os
from api.storage import threads_collection, users_collection,runs_collection, assistants_collection,messages_collection


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)
router = APIRouter()

#  Criar uma nova thread
@router.post("/threads", response_model=Thread)
async def create_thread(email: str = Body(..., embed=True)):
    """Cria uma nova thread"""
    thread = client.beta.threads.create()
    new_thread = await threads_collection.create_thread(thread)
    await users_collection.add_thread_to_user(email,thread.id)
    
    return new_thread

@router.get("/threads")
async def list_threads(email:str):
    threads_ids = await users_collection.get_user_threads(email)
    print(threads_ids)
    return threads_ids.threads

#  Enviar mensagem para a thread
@router.post("/threads/{thread_id}/messages", response_model=Message)
async def send_message(thread_id: str, role: str = Body(..., embed=True), content: str = Body(..., embed=True)):

    """Envia uma mensagem para uma thread"""

    message = client.beta.threads.messages.create(
    thread_id=thread_id,
    role=role,  # "user" para usuário, "assistant" para assistente
    content=content
    )
    message.content = content
    new_message_obj = await messages_collection.create_message(message)
    returns = await threads_collection.update_thread_message(message.id, thread_id)
    
    return new_message_obj


#  Rodar a thread (executar resposta do assistente)
@router.post("/threads/{thread_id}/{assistant_id}/run", response_model=Message)
async def run_thread(thread_id: str, assistant_id: str):
        """Executa uma thread e retorna a resposta do assistente"""

        #  Criar a execução da thread
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )
        await runs_collection.create_run(run)

        # Aguardar até a execução ser concluída
        for _ in range(15):  # Tempo máximo de espera (~30s)
            run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

            if run_status.status == "completed":
                break
            elif run_status.status in ["failed", "cancelled"]:
                raise HTTPException(status_code=400, detail=f"Execução falhou: {run_status.status}")

            time.sleep(2)  # Espera 2 segundos antes de checar novamente

        #  Buscar a resposta do assistente
        await runs_collection.update_run_status(run.id,run_status.status)
        messages = client.beta.threads.messages.list(thread_id=thread_id)

        for msg in messages.data:  # Pegar a última resposta do assistente
            if msg.role == "assistant":
                #  Extrair corretamente os blocos de texto
                content_text = " ".join(
                                block.text.value for block in msg.content)
                messages = Message(
                    id=msg.id,
                    thread_id=thread_id,
                    assistant_id=assistant_id,
                    role=msg.role,
                    content=content_text.strip(), 
                    timestamp=datetime.now()
                )
                
        await messages_collection.create_message(messages)
        await threads_collection.update_thread_message(messages.id, thread_id)
        await threads_collection.update_thread_runs(run.id, thread_id)
        return messages

                


@router.get("/threads/{thread_id}/messages", response_model=List[Message])
async def list_messages(thread_id: str):
    """Lista todas as mensagens de uma thread"""

    messages_list =  await messages_collection.get_messages_by_thread(thread_id)
    
    return messages_list




