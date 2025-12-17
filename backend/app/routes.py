from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from app.database import SessionLocal
from app.models import Document
from app.pdf_utils import get_file_hash, extract_text, chunk_text
from app.storage import upload_pdf, download_pdf
from app.rag import answer_question
import uuid, io, os, json

router = APIRouter()

DATA_ROOT = "/tmp/data"

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="PDF only")

    pdf_bytes = await file.read()
    file_hash = get_file_hash(pdf_bytes)

    db = SessionLocal()
    existing = db.query(Document).filter_by(file_hash=file_hash).first()
    if existing:
        return {"document_id": str(existing.id), "existing": True}

    doc = Document(file_hash=file_hash, file_name=file.filename)
    db.add(doc)
    db.commit()
    db.refresh(doc)

    upload_pdf(str(doc.id), pdf_bytes)

    text = extract_text(pdf_bytes)
    chunks = chunk_text(text)

    doc_dir = f"{DATA_ROOT}/{doc.id}"
    os.makedirs(doc_dir, exist_ok=True)

    with open(f"{doc_dir}/chunks.json", "w") as f:
        json.dump(chunks, f)

    return {"document_id": str(doc.id), "existing": False}

@router.post("/chat")
def chat(payload: dict):
    question = payload.get("question")
    document_id = payload.get("document_id")

    chunks_path = f"{DATA_ROOT}/{document_id}/chunks.json"
    if not os.path.exists(chunks_path):
        raise HTTPException(status_code=404, detail="Document not indexed")

    with open(chunks_path) as f:
        chunks = json.load(f)

    answer = answer_question(question, chunks)
    return {"answer": answer}

@router.get("/documents/{document_id}/download")
def download(document_id: str):
    pdf_bytes = download_pdf(document_id)
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=document.pdf"}
    )
