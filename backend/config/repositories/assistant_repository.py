from datetime import datetime
from pymongo.errors import PyMongoError
from config.models import Assistant
from motor.motor_asyncio import AsyncIOMotorClient


#Classe para manipular os dados do assistant com o mongo 
class MongoAssistantRepository():
    def __init__(self, client: AsyncIOMotorClient):
        self.collection = client.assistants
    
    async def create_assistant(self, new_assistant: Assistant, max_tokens: int):
        try:
            document =  await self.collection.insert_one({"id":new_assistant.id,
                                                        "name":new_assistant.name,
                                                        "instructions":new_assistant.instructions,
                                                        "model":new_assistant.model,
                                                        "tools": [],
                                                        "tools_resources":[],
                                                        "threads": [],
                                                        "temperature":new_assistant.temperature,
                                                       " max_tokens": max_tokens,
                                                        "top_p":new_assistant.top_p})
            return True if document else None
        except PyMongoError as e:
            print(f"Erro ao registrar assistant: {e}")
             
    async def get_assistant(self, assistant_id: str):
        try:
            document =  await self.collection.find_one({"id":assistant_id})
            return self.__to_assistant_model(document) if document else None
       
        except PyMongoError as e:
            print(f"Erro ao pegar assistant: {e}") 

    async def update_assistant(self, update_assistant: Assistant):
        try:
            result = await self.collection.update_one({"id": update_assistant.id},
                                                        {"$set": {"name":update_assistant.name,
                                                        "instructions":update_assistant.instructions,
                                                        "model":update_assistant.model,
                                                        "tools": update_assistant.tools,
                                                        "tools_resources": update_assistant.tools_resources,
                                                        "threads": update_assistant.threads,
                                                        "temperature":update_assistant.temperature,
                                                        "threads": update_assistant.threads,
                                                       " max_tokens": update_assistant.max_tokens,
                                                        "top_p":update_assistant.top_p}})
            return result
        except PyMongoError as e:
            print(f"Erro ao up usuário: {e}") 

    async def delete_assistant(self, assistant_id: str):
        try:
            result = await self.collection.delete_one({"id": assistant_id})
            return result.deleted_count > 0  # Retorna True se o assistente foi deletado
        except PyMongoError as e:
            print(f"Erro ao excluir assistant: {e}")
            return None
        
    async def update_assistant_thread(self, new_thread_id: str, assistant_id: str):
        try:
            result = await self.collection.update_one({"id": assistant_id},
                    
                                                  {"$push": {"threads": new_thread_id}})
            return result
                
        except PyMongoError as e:
            print(f"Erro ao adicionar assistant thread: {e}")
            return None
    
    async def delete_assistant_thread(self, thread_id: str, assistant_id: str):
        try:
            result = await self.thread_collection.update_one(
                {"id": assistant_id},
                {"$pull": {"threads": thread_id}}
            )
            if result.deleted_count > 0:
                return result
            return False
        except PyMongoError as e:
            print(f"Erro ao excluir thread no assistant: {e}")

        return None
    def __to_assistant_model(self, obj: dict[str,any]) -> Assistant:
        return Assistant(
            id=obj["id"],
            name=obj["name"],
            instructions=obj["instructions"],
            model=obj["model"],
            tools=obj.get("tools",[]),
            tools_resources=obj.get("tools_resources",[]),
            threads=obj["threads"],
            temperature=obj["temperature"],
            max_tokens= obj["max_tokens"],
            top_p=obj["top_p"],
        )