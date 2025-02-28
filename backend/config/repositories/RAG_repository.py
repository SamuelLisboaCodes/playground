from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError
from config.models import RagUserFiles, RagVectorStore, Thread  # Importando a classe Thread do arquivo models.py

class MongoRAGRepository:
    def __init__(self, client: AsyncIOMotorClient):
        """Inicializa a conexão com a coleção 'threads' no banco 'playground_DB'."""
        self.collection = client.threads

    async def create_vector_store(self, new_vector: RagVectorStore):
        """Cria uma nova thread no banco de dados."""
        try:
            document = await self.collection.insert_one({
                "vector_id": new_vector.id,
                "name": new_vector.name,
                "file_ids": new_vector.get("file_ids",[])
            })

            return await self.get_vector_store(new_vector.id) if document.inserted_id else None
        except PyMongoError as e:
            print(f"Erro ao registrar thread: {e}")
            return None

    async def get_vector_store(self, vector_id: str):
        
        try:
            document = await self.collection.find_one({"vector_id": vector_id})
            return self.__to_thread_model(document) if document else None
        except PyMongoError as e:
            print(f"Erro ao obter thread: {e}")
            return None
        
    async def update_vector_store(self, update_vector: RagVectorStore):
        
        try:
            result = await self.collection.update_one(
                {"vector_id": update_vector.id},
                {"$addToSet": {
                    "file_ids": update_vector.get("file_ids"),
                }}
            )
            return result.modified_count > 0  # Retorna True se houve atualização
        except PyMongoError as e:
            print(f"Erro ao atualizar thread: {e}")
            return None
    async def create_user_files(self, new_file: RagUserFiles):
        try:
            document = await self.collection.insert_one({
            "file_id": new_file.id,
            "purpose": new_file.purpose,
            "file_attach": new_file.file_attach
        })

            return await self.get_vector_store(new_file.id) if document.inserted_id else None
        except PyMongoError as e:
            print(f"Erro ao registrar thread: {e}")
            return None
    async def delete_thread(self, thread_id: str):
        
        try:
            result = await self.collection.delete_one({"id": thread_id})
            return result.deleted_count > 0  # Retorna True se a thread foi deletada
        except PyMongoError as e:
            print(f"Erro ao excluir thread: {e}")
            return None
    async def update_assistant_thread(self, thread_id: str, assistant_id: str):
        try:
            result = await self.collection.update_one({"id": thread_id},
                    
                                                  {"$set": {"assistant_id": assistant_id}})
            return result
                
        except PyMongoError as e:
            print(f"Erro ao adicionar assistant thread: {e}")
            return None
        
    async def update_thread_message(self, new_message_id: str, thread_id: str):
        try:
            result = await self.collection.update_one({"id": thread_id},
                    
                                                  {"$push": {"messages": new_message_id}})
            return result
                
        except PyMongoError as e:
            print(f"Erro ao adicionar thread message: {e}")
            return None
        
    async def delete_thread_message(self, message_id: str, thread_id: str):

        try:
            result = await self.thread_collection.update_one(
                    {"id": thread_id},
                    {"$pull": {"messages": message_id}}
                )
            if result.deleted_count > 0:
                return result
            return False
        except PyMongoError as e:
            print(f"Erro ao excluir mensagem na thread: {e}")
            return None
    
    async def update_thread_runs(self, new_run_id: str, thread_id: str):
        try:
            result = await self.collection.update_one({"id": thread_id},
                    
                                                  {"$push": {"threads": new_run_id}})
            return result
                
        except PyMongoError as e:
            print(f"Erro ao adicionar thread run: {e}")
            return None
        

    def __to_thread_model(self, obj: dict) -> Thread:
        """Converte um documento do MongoDB para um objeto Thread."""
        return Thread(
            id=obj["id"],
            messages=obj.get("messages", []),
            runs=obj.get("runs", [])
        )