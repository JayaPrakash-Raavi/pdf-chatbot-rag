import faiss
import numpy as np
import json
from fastembed import TextEmbedding
from app.storage import download_file
from app.llm import generate_answer

embedder = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")


def load_index_and_chunks(document_id: str):
    index_bytes = download_file(f"{document_id}/faiss.index")
    chunks_bytes = download_file(f"{document_id}/chunks.json")

    index = faiss.deserialize_index(index_bytes)
    chunks = json.loads(chunks_bytes.decode())

    return index, chunks


def answer_question(question: str, document_id: str, k: int = 5):
    index, chunks = load_index_and_chunks(document_id)

    query_embedding = np.array(
        list(embedder.embed([question]))
    ).astype("float32")

    distances, indices = index.search(query_embedding, k)

    retrieved_chunks = [chunks[i] for i in indices[0]]
    context = "\n\n".join(retrieved_chunks)

    return generate_answer(question, context)
