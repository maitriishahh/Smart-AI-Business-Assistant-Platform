from sentence_transformers import SentenceTransformer
from backend.app.rag.vector_store import store_vectors

model = SentenceTransformer("all-MiniLM-L6-v2")

async def generate_embeddings(
        chunks, user_id, filename
):
    embeddings = model.encode(chunks).tolist()

    await store_vectors(
        chunks=chunks,
        embeddings=embeddings,
        user_id=user_id,
        filename=filename
    )

    