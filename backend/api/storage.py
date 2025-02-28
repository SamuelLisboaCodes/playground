from  motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from config.models import User
import os

from config.repositories.assistant_repository import MongoAssistantRepository
from config.repositories.message_repository import MongoMessageRepository
from config.repositories.threads_repository import MongoThreadRepository
from config.repositories.user_repository import MongoUserRepository
from config.repositories.run_repository import MongoRunRepository
from config.repositories.RAG_repository import MongoRAGRepository

load_dotenv()


mongodb_uri = os.getenv("MONGODB_URI")
mongo_db_client = AsyncIOMotorClient(mongodb_uri)["playground_DB"]

users_collection = MongoUserRepository(mongo_db_client)
assistants_collection = MongoAssistantRepository(mongo_db_client)
threads_collection = MongoThreadRepository(mongo_db_client)
messages_collection = MongoMessageRepository(mongo_db_client)
runs_collection = MongoRunRepository(mongo_db_client)
rag_collection = MongoRAGRepository(mongo_db_client)

