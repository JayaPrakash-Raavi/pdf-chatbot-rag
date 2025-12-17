from supabase import create_client
from app.config import SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, SUPABASE_BUCKET

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def upload_pdf(document_id: str, file_bytes: bytes):
    path = f"{document_id}/original.pdf"
    supabase.storage.from_(SUPABASE_BUCKET).upload(
        path,
        file_bytes,
        {"content-type": "application/pdf"}
    )
    return path

def download_pdf(document_id: str):
    path = f"{document_id}/original.pdf"
    return supabase.storage.from_(SUPABASE_BUCKET).download(path)
