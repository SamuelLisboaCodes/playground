from fastapi import FastAPI, Request, Response, HTTPException
from dotenv import load_dotenv
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
import os
from api import auth, agents, threads 

load_dotenv()

app = FastAPI(title="OpenAI Assistants API")

SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(agents.router, prefix="/api", tags=["agents"])
app.include_router(threads.router, prefix="/api", tags=["threads"])

@app.middleware("http")
async def some_middleware(request: Request, call_next):
    response = await call_next(request)
    return response

# Rota principal
@app.get("/")
async def root():
    return {"message": "API FastAPI rodando!"}

# Rota de usuário autenticado
@app.get('/user')
async def user_info(request: Request):
    if "session" not in request.cookies:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {"message": "Usuário autenticado", "token": 'token'}

# Rota de logout
@app.post('/logout')
async def logout(response: Response):
    response.delete_cookie(key="session")
    return {"message": "Logout realizado com sucesso"}
