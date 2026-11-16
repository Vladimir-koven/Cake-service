from fastapi import FastAPI

app = FastAPI(title="Cake AI Service")


@app.get("/")
async def root():
    return {"message": "Service is running"}
