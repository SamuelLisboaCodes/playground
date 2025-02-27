from fastapi import FastAPI, Request
from dotenv import load_dotenv
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

import os
from api import auth,agents,threads

load_dotenv()
app = FastAPI()
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(agents.router, prefix="/api", tags=["agents"])
app.include_router(threads.router, prefix="/api", tags=["threads"])

 
@app.get("/")
async def root():
    return {"message": "API FastAPI rodando"}


    