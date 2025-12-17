from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Hybrid Resume Chatbot")

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}
