from fastapi import FastAPI, Request
from dotenv import load_dotenv
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

import os
from api import auth 
from api.agents import router as assistants_router
from api.threads import router as threads_router
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

 
@app.get("/")
async def root():
    return {"message": "API FastAPI rodando"}
    
app.include_router(assistants_router, prefix="/api")
app.include_router(threads_router, prefix="/api")
