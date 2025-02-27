from fastapi import FastAPI, Request
from dotenv import load_dotenv
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
import os
from backend.api import auth 
from backend.api.agents import router as assistants_router
from backend.api.threads import router as threads_router
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Minha API",
        version="1.0.0",
        description="Documentação atualizada da API",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


load_dotenv()
app = FastAPI()

app.openapi = custom_openapi

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
    
app.include_router(assistants_router, prefix="/api")
app.include_router(threads_router, prefix="/api")
