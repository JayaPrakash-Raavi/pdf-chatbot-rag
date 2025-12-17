from supabase import create_client
from app.config import (
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY,
    SUPABASE_BUCKET
)

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def upload_file(path: str, content: bytes, content_type: str):
    supabase.storage.from_(SUPABASE_BUCKET).upload(
        path,
        content,
        {"content-type": content_type}
    )

def download_file(path: str) -> bytes:
    return supabase.storage.from_(SUPABASE_BUCKET).download(path)

def upload_pdf(document_id: str, file_bytes: bytes):
    upload_file(
        f"{document_id}/original.pdf",
        file_bytes,
        "application/pdf"
    )

def download_pdf(document_id: str) -> bytes:
    return download_file(f"{document_id}/original.pdf")
