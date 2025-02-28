from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError
from config.models import RagUserFiles, RagVectorStore, Thread  # Importando a classe Thread do arquivo models.py

class MongoRAGRepository:
    def __init__(self, client: AsyncIOMotorClient):
        """Inicializa a conexão com a coleção 'RAG' no banco 'test_playground_DB'."""
        self.collection = client.rags

    async def create_vector_store(self, new_vector: RagVectorStore):
        """Cria um novo vector no banco de dados."""
        try:
            document = await self.collection.insert_one({
                "vector_id": new_vector.id,
                "name": new_vector.name,
                "file_ids": new_vector.get("file_ids",[])
            })
    
            return await self.get_vector_store(new_vector.id) if document.vector_id else None
        except PyMongoError as e:
            print(f"Erro ao registrar vector_store: {e}")
            return None

    async def get_vector_store(self, vector_id: str):
        
        try:
            document = await self.collection.find_one({"vector_id": vector_id})
            return self.__to_vector_store_model(document) if document else None
        except PyMongoError as e:
            print(f"Erro ao obter vector_store: {e}")
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
            print(f"Erro ao atualizar vector_store: {e}")
            return None
    async def create_user_files(self, new_file: RagUserFiles):
        try:
            document = await self.collection.insert_one({
            "file_id": new_file.id,
            "user_email": new_file.user_email,
            "purpose": new_file.purpose,
            "file_attach": new_file.file_attach
        })

            return await self.get_user_file(new_file.id) if document.file_id else None
        except PyMongoError as e:
            print(f"Erro ao registrar files: {e}")
            return None
        
    async def get_user_file(self, file_id: str):
        
        try:
            document = await self.collection.find_one({"file_id": file_id})
            return self.__to_files_model(document) if document else None
        except PyMongoError as e:
            print(f"Erro ao obter file: {e}")
            return None
        
    async def delete_user_file(self, file_id: str):
        
        try:
            result = await self.collection.delete_one({"file_id": file_id})
            return result.deleted_count > 0  # Retorna True se a thread foi deletada
        except PyMongoError as e:
            print(f"Erro ao excluir file: {e}")


    def __to_vector_store_model(self, obj: dict) -> RagVectorStore:
        """Converte um documento do MongoDB para um objeto Vector_Store."""
        return RagVectorStore(
            vector_id = obj["vector_id"],
            name= obj["name"],
            file_ids= obj["file_ids"]
        )

    def __to_files_model(self, obj: dict) -> RagUserFiles:
        """Converte um documento do MongoDB para um objeto RagUserFiles."""
        return RagUserFiles(
            files_id=obj["files_id"],
            purpose=obj.get("purpose"),
            user_email=obj.get("user_email"),
            file_attach=obj["file_attach"]
        )