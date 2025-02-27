from datetime import datetime
from pymongo.errors import PyMongoError
from config.models import User
from motor.motor_asyncio import AsyncIOMotorClient


#Classe para manipular os dados de usuario com o mongo 
class MongoUserRepository():
    def __init__(self, client: AsyncIOMotorClient):
        self.collection = client.users
    
    async def create_user(self, user_id: str, user_email: str):
        try:
            document =  await self.collection.insert_one({"id": user_id,
                                                         "email": user_email,
                                                         "refresh_token": '',
                                                         "assistants": [],
                                                         "threads": []})
            return True if document else None
        except PyMongoError as e:
            print(f"Erro ao registrar usuário: {e}") 

    async def get_user(self, user_id: str):
        try:
            document =  await self.collection.find_one({"id":user_id})
            return self.__to_user_model(document) if document else None
       
        except PyMongoError as e:
            print(f"Erro ao get usuário: {e}") 

    async def get_user_assistants(self, user_email: str):
        try:
            document =  await self.collection.find_one({"email":user_email})
            return document["assistants"] if document else None
       
        except PyMongoError as e:
            print(f"Erro ao get usuário: {e}") 

    async def add_thread_to_user(self, user_email: str, thread_id:str):
        try:
            result = await self.collection.update_one({"email": user_email},
            {"$addToSet": {"threads": thread_id}})
            return result
        except PyMongoError as e:
            print(f"Erro ao up usuário: {e}")

    async def update_user_token(self, user_email: str, refresh_token:str):
        try:
            result = await self.collection.update_one({"email": user_email},
            {"$set": {"refresh_token": refresh_token}})
            return result
        except PyMongoError as e:
            print(f"Erro ao up usuário: {e}") 

    async def add_assistant_to_user(self, user_email: str, assistant_id: str):
        """Adiciona um assistente à lista de assistentes do usuário."""
        try:
            result = await self.collection.update_one(
                {"email": user_email},
                {"$addToSet": {"assistants": assistant_id}}  # Evita duplicação
            )
            return result.modified_count > 0
        except PyMongoError as e:
            print(f"Erro ao adicionar assistente ao usuário: {e}")
            return None

    async def remove_assistant_from_user(self, user_id: str, assistant_id: str):
        """Remove um assistente da lista de assistentes do usuário."""
        try:
            result = await self.collection.update_one(
                {"id": user_id},
                {"$pull": {"assistants": assistant_id}}  # Remove a referência do assistente
            )
            return result.modified_count > 0
        except PyMongoError as e:
            print(f"Erro ao remover assistente do usuário: {e}")
            return None
        
    async def remove_thread_from_user(self, user_id: str, thread_id: str):
        """Remove um assistente da lista de assistentes do usuário."""
        try:
            result = await self.collection.update_one(
                {"id": user_id},
                {"$pull": {"threads": thread_id}}  # Remove a referência do assistente
            )
            return result.modified_count > 0
        except PyMongoError as e:
            print(f"Erro ao remover assistente do usuário: {e}")
            return None    
    def __to_user_model(self, obj: dict[str,any]) -> User:
        return User(
            id = obj["id"],
            email= obj["email"],
            refresh_token = obj["refresh_token"],
            assistants= obj["assistants"],
            threads = obj["threads"]
        )