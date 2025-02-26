from fastapi import FastAPI, Request
from dotenv import load_dotenv
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
import os
from api import auth,agents,threads
load_dotenv()
app = FastAPI()
app.include_router(auth.router, prefix="/auth", tags=["auth"])
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

@app.middleware("http")
async def some_middleware(request: Request, call_next):
    response = await call_next(request)
    return response
 
@app.get("/")
async def login():
    return {"message": "API FastAPI rodando"}
@app.get('/user')
async def user_info(request: Request):
    print(request.cookies)
    return {"message": "Usuário autenticado", "token": 'token'}
    