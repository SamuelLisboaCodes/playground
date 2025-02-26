from fastapi import FastAPI, Request
from dotenv import load_dotenv
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
import os
from api import auth,agents,threads
load_dotenv()
app = FastAPI()
app.include_router(auth.router, prefix="/auth", tags=["auth"])


 
@app.get("/")
async def login():
    return {"message": "API FastAPI rodando"}


    