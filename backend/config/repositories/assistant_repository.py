from datetime import datetime
from pymongo.errors import PyMongoError
from config.models import Assistant
from motor.motor_asyncio import AsyncIOMotorClient


#Classe para manipular os dados do assistant com o mongo 
class MongoAssistantRepository():
    def __init__(self, client: AsyncIOMotorClient):
        self.collection = client.assistants
    
    async def create_assistant(self, new_assistant: Assistant):
        try:
            document =  await self.collection.insert_one({"id":new_assistant.id,
                                                        "name":new_assistant.name,
                                                        "instructions":new_assistant.instructions,
                                                        "model":new_assistant.model,
                                                        "tools": [],
                                                        "tools_resources":[],
                                                        "temperature":new_assistant.temperature,
                                                        "top_p":new_assistant.top_p})
            return await self.get_assistant(new_assistant.id) if document else None
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
                                                        "temperature":update_assistant.temperature,
                                                        "threads": update_assistant.threads,
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
        
    
    def __to_assistant_model(self, obj: dict) -> Assistant:
        return Assistant(
            id=obj["id"],
            name=obj["name"],
            instructions=obj["instructions"],
            model=obj["model"],
            tools=obj.get("tools",[]),
            tools_resources=obj.get("tools_resources",[]),
            temperature=obj["temperature"],
            top_p=obj["top_p"],
        )