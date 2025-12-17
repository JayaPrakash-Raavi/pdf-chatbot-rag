from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Document
from app.pdf_utils import get_file_hash, extract_text, chunk_text
from app.storage import upload_pdf, download_pdf
from app.rag import build_and_store_index, answer_question
import io

router = APIRouter()


# -------------------------
# Upload PDF + Build RAG
# -------------------------
@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    pdf_bytes = await file.read()
    file_hash = get_file_hash(pdf_bytes)

    db: Session = SessionLocal()

    try:
        # Check for existing document (deduplication)
        existing = db.query(Document).filter_by(file_hash=file_hash).first()
        if existing:
            return {
                "document_id": str(existing.id),
                "existing": True
            }

        # Create DB record
        doc = Document(
            file_hash=file_hash,
            file_name=file.filename
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)

        document_id = str(doc.id)

        # Store PDF permanently
        upload_pdf(document_id, pdf_bytes)

        # Extract + chunk text
        text = extract_text(pdf_bytes)
        chunks = chunk_text(text)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No readable text found in PDF"
            )

        # Build embeddings + FAISS and store in Supabase
        build_and_store_index(document_id, chunks)

        return {
            "document_id": document_id,
            "existing": False
        }

    finally:
        db.close()


# -------------------------
# Chat Endpoint (RAG)
# -------------------------
@router.post("/chat")
def chat(payload: dict):
    question = payload.get("question")
    document_id = payload.get("document_id")

    if not question or not document_id:
        raise HTTPException(
            status_code=400,
            detail="Both 'question' and 'document_id' are required"
        )

    answer = answer_question(question, document_id)

    return {
        "answer": answer
    }


# -------------------------
# Download Original PDF
# -------------------------
@router.get("/documents/{document_id}/download")
def download(document_id: str):
    pdf_bytes = download_pdf(document_id)

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=document.pdf"
        }
    )
