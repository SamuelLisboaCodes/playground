from datetime import datetime
from pymongo.errors import PyMongoError
from config.models import User
from motor.motor_asyncio import AsyncIOMotorClient


#Classe para manipular os dados de usuario com o mongo 
class MongoUserRepository():
    def __init__(self, client: AsyncIOMotorClient):
        self.collection = client.playground_DB.users
    
    async def create_user(self, user_id: str, user_email: str):
        try:
            document =  await self.collection.insert_one({"id": user_id,
                                                         "email": user_email,
                                                         "refresh_token": '',
                                                         "created_at": datetime.now(),
                                                         "assistants": []})
            return True if document else None
        except PyMongoError as e:
            print(f"Erro ao registrar usuário: {e}") 
    async def get_user(self, user_id: str):
        try:
            document =  await self.collection.find_one({"id":user_id})
            return self.__to_user_model(document) if document else None
       
        except PyMongoError as e:
            print(f"Erro ao get usuário: {e}") 

    async def update_user_token(self, user_id: str, refresh_token:str):
        try:
            result = await self.collection.update_one({"id": user_id},
            {"$set": {"refresh_token": refresh_token}})
            return result
        except PyMongoError as e:
            print(f"Erro ao up usuário: {e}") 

    def __to_user_model(self, obj: dict[str,any]) -> User:
        return User(
            id = obj["id"],
            email= obj["email"],
            refresh_token = obj["refresh_token"],
            assistants= obj["assistants"],
        )