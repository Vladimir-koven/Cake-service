from fastapi import FastAPI

from app.api.v1.chat import router as chat_router

app = FastAPI(title="Cake AI Service")
app.include_router(chat_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Service is running"}
