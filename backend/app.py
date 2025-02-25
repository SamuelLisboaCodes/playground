from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.responses import RedirectResponse


from api import auth
load_dotenv()
app = FastAPI()
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
async def login():
    return {"message": "API FastAPI rodando"}
@app.get('/user')
async def user_info(token: str):
    return {"message": "Usuário autenticado", "token": token}
    