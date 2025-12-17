import faiss
import numpy as np
import json
from fastembed import TextEmbedding
from app.storage import upload_file, download_file
from app.llm import generate_answer

embedder = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")


def build_and_store_index(document_id: str, chunks: list[str]):
    """
    Build FAISS index from chunks and store it in Supabase Storage
    """

    embeddings = list(embedder.embed(chunks))
    embeddings = np.array(embeddings).astype("float32")

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # Serialize FAISS index
    index_bytes = faiss.serialize_index(index)

    # Upload index + chunks to Supabase
    upload_file(f"{document_id}/faiss.index", index_bytes)
    upload_file(
        f"{document_id}/chunks.json",
        json.dumps(chunks).encode("utf-8")
    )


def load_index_and_chunks(document_id: str):
    """
    Load FAISS index and chunks from Supabase Storage
    """
    index_bytes = download_file(f"{document_id}/faiss.index")
    chunks_bytes = download_file(f"{document_id}/chunks.json")

    index = faiss.deserialize_index(index_bytes)
    chunks = json.loads(chunks_bytes.decode("utf-8"))

    return index, chunks


def answer_question(question: str, document_id: str, k: int = 5):
    """
    RAG pipeline:
    - embed question
    - FAISS search
    - send context to Groq
    """
    index, chunks = load_index_and_chunks(document_id)

    query_embedding = np.array(
        list(embedder.embed([question]))
    ).astype("float32")

    distances, indices = index.search(query_embedding, k)

    retrieved_chunks = [chunks[i] for i in indices[0]]
    context = "\n\n".join(retrieved_chunks)

    return generate_answer(question, context)
