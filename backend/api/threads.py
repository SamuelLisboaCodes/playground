#%%
from fastapi import APIRouter, HTTPException
from openai import OpenAI
from config.models import Thread, Message, Run
from datetime import datetime
from typing import List
from dotenv import load_dotenv
import time
import os
from dotenv import load_dotenv
<<<<<<< HEAD
from api.storage import threads_collection, users_collection,runs_collection, assistants_collection,messages_collection



=======




>>>>>>> bb4a5f23d2aa4aa24c7af81da6df0ceb6bd2693e
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)
router = APIRouter()
#%%
#  Criar uma nova thread
@router.post("/threads", response_model=Thread)
async def create_thread(user_email: str):
    """Cria uma nova thread associada a um assistente"""
    thread = client.beta.threads.create()
    new_thread = await threads_collection.create_thread(thread)
    await users_collection.add_thread_to_user(user_email,thread.id)
    
    return new_thread

<<<<<<< HEAD
=======
    return Thread(
        id=thread.id,
        assistant_id=assistant_id,
        messages=[],
        runs=[]
    )



>>>>>>> bb4a5f23d2aa4aa24c7af81da6df0ceb6bd2693e
#  Enviar mensagem para a thread
@router.post("/threads/{thread_id}/messages", response_model=Message)
async def send_message(thread_id: str, role: str, content: str):
    '''
        Message(
    id=message.id,
    thread_id=thread_id,
    role=role,
    content=content,
    timestamp=datetime.utcnow()
    )
    '''
    """Envia uma mensagem para uma thread"""
    try:
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role=role,  # "user" para usuário, "assistant" para assistente
            content=content
        )
        new_message_obj = await messages_collection.create_message(message)
        return new_message_obj

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

#  Rodar a thread (executar resposta do assistente)
@router.post("/threads/{thread_id}/run", response_model=Message)
async def run_thread(thread_id: str, assistant_id: str):
    """Executa uma thread e retorna a resposta do assistente"""
    try:
        # 🔹 Criar a execução da thread
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )
        await runs_collection.create_run(run)

        # 🔄 Aguardar até a execução ser concluída
        for _ in range(15):  # Tempo máximo de espera (~30s)
            run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)

            if run_status.status == "completed":
                break
            elif run_status.status in ["failed", "cancelled"]:
                raise HTTPException(status_code=400, detail=f"Execução falhou: {run_status.status}")

            time.sleep(2)  # Espera 2 segundos antes de checar novamente
        await runs_collection.update_run_status(run_status)
        # 🔹 Buscar a resposta do assistente
        messages = client.beta.threads.messages.list(thread_id=thread_id)

        for msg in messages.data:  # Pegar a última resposta do assistente
            if msg.role == "assistant":
                # 🔹 Extrair corretamente os blocos de texto
                content_text = " ".join(
                                block.text.value for block in msg.content)
                new_message = Message(
                    id=msg.id,
                    thread_id=thread_id,
                    role=msg.role,
                    content=content_text.strip(),  # Agora é uma string válida
                    timestamp=datetime.now(datetime.timezone.utc)
                )
                await messages_collection.update_message(new_message)
                return new_message

        # Se não encontrou resposta, lançar erro
        raise HTTPException(status_code=400, detail="Nenhuma resposta do assistente encontrada.")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/threads/{thread_id}/messages", response_model=List[Message])
async def list_messages(thread_id: str):
    """Lista todas as mensagens de uma thread"""
    try:
        messages_list = await threads_collection.get_messages_by_thread(thread_id)
        return messages_list
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        '''
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        formatted_messages = []
        for msg in messages.data:
            content_text = " ".join(
                block.text.value for block in msg.content)

            formatted_message = Message(
                id=msg.id,
                thread_id='thread_PZbs924Euhlu2ocJ4IT1aZgr',
                role=msg.role,
                content=content_text,
                timestamp=datetime.fromtimestamp(msg.created_at)
            )

            formatted_messages.append(formatted_message)
            

        return formatted_messages
        '''

<<<<<<< HEAD
=======
        return formatted_messages

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
>>>>>>> bb4a5f23d2aa4aa24c7af81da6df0ceb6bd2693e

#%%