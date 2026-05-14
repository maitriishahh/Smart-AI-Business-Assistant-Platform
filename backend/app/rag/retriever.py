from sentence_transformers import SentenceTransformer
from backend.app.rag.vector_store import retrieve_documents

model = SentenceTransformer("all-MiniLM-L6-v2")

async def retrieve_relevant_chunks(
        question: str,
        user_id: str
):
    query_embedding = model.encode(question).tolist()
    
    documents = await retrieve_documents(query_embedding=query_embedding, user_id=user_id)

    return documents