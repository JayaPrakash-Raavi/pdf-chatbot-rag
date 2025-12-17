import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.database import SessionLocal
from app.models import Document
from app.pdf_utils import get_file_hash

router = APIRouter()

BASE_URL = os.getenv("BASE_URL")

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    db = SessionLocal()

    try:
        pdf_bytes = await file.read()
        file_hash = get_file_hash(pdf_bytes)

        existing = (
            db.query(Document)
            .filter(Document.file_hash == file_hash)
            .first()
        )

        if existing:
            return {
                "chatbot_url": f"{BASE_URL}/chat/{existing.id}",
                "existing": True
            }

        doc = Document(
            file_hash=file_hash,
            file_name=file.filename
        )

        db.add(doc)
        db.commit()
        db.refresh(doc)

        return {
            "chatbot_url": f"{BASE_URL}/chat/{doc.id}",
            "existing": False
        }

    finally:
        db.close()
