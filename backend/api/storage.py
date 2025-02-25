from  motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from config.models import User
import os

load_dotenv()


mongodb_uri = os.getenv("MONGODB_URI")
mongo_db_client = AsyncIOMotorClient(mongodb_uri)





