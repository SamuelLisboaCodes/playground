from fastapi import FastAPI
from backend.api.agents import router as assistants_router
from backend.api.threads import router as threads_router
app = FastAPI(title="OpenAI Assistants API")

app.include_router(assistants_router, prefix="/api")
app.include_router(assistants_router, prefix="/api")
app.include_router(threads_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "API rodando!"}