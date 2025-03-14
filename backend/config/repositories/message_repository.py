import json
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError
from config.models import Message  # Importando a classe Message do arquivo models.py
from datetime import datetime
class MongoMessageRepository:
    def __init__(self, client: AsyncIOMotorClient):
        """Inicializa a conexão com a coleção 'messages' no banco 'playground_DB'."""
        self.collection = client.messages

    async def create_message(self, new_message: Message):
        """Cria uma nova mensagem no banco de dados."""
        try:
            document = await self.collection.insert_one({
                "id": new_message.id,
                "thread_id": new_message.thread_id,
                "assistant_id": new_message.assistant_id,
                "role": new_message.role,
                "content": new_message.content,
                "timestamp": datetime.now()
            })
            return await self.get_message(new_message.id) if document else None
        except PyMongoError as e:
            print(f"Erro ao registrar mensagem: {e}")
            return None

    async def get_message(self, message_id: str):
        """Obtém uma mensagem pelo ID."""
        try:
            document = await self.collection.find_one({"id": message_id})
            return self.__to_message_model(document) if document else None
        except PyMongoError as e:
            print(f"Erro ao obter mensagem: {e}")
            return None

    async def update_message(self, updated_message: Message):
        """Atualiza os dados de uma mensagem no banco de dados."""
        try:
            result = await self.collection.update_one(
                {"id": updated_message.id},
                {"$set": {
                    "thread_id": updated_message.thread_id,
                    "assistant_id": updated_message.assistant_id,
                    "role": updated_message.role,
                    "content": updated_message.content,
                    "timestamp": updated_message.timestamp
                }}
            )
            return result.modified_count > 0  # Retorna True se houve atualização
        except PyMongoError as e:
            print(f"Erro ao atualizar mensagem: {e}")
            return None

    async def delete_message(self, message_id: str):
        #Remove uma mensagem e também a desvincula da thread correspondente.
        try:
            # Obtém a mensagem para saber a qual thread pertence  # Se a mensagem não existe, retorna Fals
            # Remove a mensagem da coleção de mensagens
            result = await self.collection.delete_one({"id": message_id})
            
            if result.deleted_count > 0:
                return result
            return False
        except PyMongoError as e:
            print(f"Erro ao excluir mensagem: {e}")
            return None
        
    async def get_messages_by_thread(self, thread_id: str):
        """Obtém todas as mensagens de uma thread pelo ID."""
        try:
            messages = []
            async for msg in self.collection.find({"thread_id": thread_id}):
                messages.append(self.__to_message_model(msg))
            return messages
        except PyMongoError as e:
            print(f"Erro ao obter mensagens da thread: {e}")
            return None
        
    def __to_message_model(self, obj: dict) -> Message:
        """Converte um documento do MongoDB para um objeto Message."""
        return Message(
            id=obj["id"],
            thread_id=obj["thread_id"],
            assistant_id=obj.get("assistant_id", None),
            role=obj["role"],
            content=obj["content"],
            timestamp=obj["timestamp"]
        )
