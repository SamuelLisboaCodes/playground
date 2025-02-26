from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError
from config.models import Run  # Importando a classe Run do arquivo models.py
from datetime import datetime
class MongoRunRepository:
    def __init__(self, client: AsyncIOMotorClient):
        """Inicializa a conexão com a coleção 'runs' no banco 'playground_DB'."""
        self.collection = client.runs

    async def create_run(self, new_run: Run):
        """Cria um novo registro de execução no banco de dados."""
        try:
            document = await self.collection.insert_one({
                "id": new_run.id,
                "thread_id": new_run.thread_id,
                "assistant_id": new_run.assistant_id,
                "status": new_run.get("status"),
                "created_at": new_run.get("status"),
            })
            return await self.collection.get_run(new_run.id) if document.inserted_id else None
        except PyMongoError as e:
            print(f"Erro ao registrar run: {e}")
            return None

    async def get_run(self, run_id: str):
        """Obtém um registro de execução pelo ID."""
        try:
            document = await self.collection.find_one({"id": run_id})
            return self.__to_run_model(document) if document else None
        except PyMongoError as e:
            print(f"Erro ao obter run: {e}")
            return None

    async def update_run(self, updated_run: Run):
        """Atualiza os dados de um registro de execução no banco de dados."""
        try:
            result = await self.collection.update_one(
                {"id": updated_run.id},
                {"$set": {
                    "thread_id": updated_run.thread_id,
                    "status": updated_run.status,
                    "created_at": updated_run.created_at,
                    "completed_at": updated_run.completed_at
                }}
            )
            return result.modified_count > 0  # Retorna True se houve atualização
        except PyMongoError as e:
            print(f"Erro ao atualizar run: {e}")
            return None
    async def update_run_status(self, run_id: str, status_run: str):
        """Atualiza os dados de um registro de execução no banco de dados."""
        try:
            result = await self.collection.update_one(
            {"id": run_id},
            {"$set": {
                "status": status_run,
                "completed_at": datetime.now(datetime.timezone.utc)
                }}
            )
            return result.modified_count > 0  # Retorna True se houve atualização
        except PyMongoError as e:
            print(f"Erro ao atualizar run: {e}")
            return None
        
    async def delete_run(self, run_id: str):
        """Remove um registro de execução do banco de dados."""
        try:
            result = await self.collection.delete_one({"id": run_id})
            return result.deleted_count > 0  # Retorna True se o run foi deletado
        except PyMongoError as e:
            print(f"Erro ao excluir run: {e}")
            return None

    def __to_run_model(self, obj: dict) -> Run:
        """Converte um documento do MongoDB para um objeto Run."""
        return Run(
            id=obj["id"],
            thread_id=obj["thread_id"],
            assistant_id=obj["assistant_id"],
            status=obj["status"],
            created_at=obj["created_at"],
            completed_at=obj.get("completed_at")
        )