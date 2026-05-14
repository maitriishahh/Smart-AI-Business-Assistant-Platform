import uuid
import chromadb

client = chromadb.PersistentClient(path="backend/app/chromadb")

collection = client.get_or_create_collection(
    name = "business_documents"
)

async def store_vectors(
        chunks,embeddings,user_id,filename
):
    ids = [str(uuid.uuid4()) for _ in chunks]

    metadatas = [{"user_id":user_id,
    "filename":filename}
    for _ in chunks]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

async def retrieve_documents(
        query_embedding, user_id
):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5,
        where={"user_id":user_id}
    )
    return results["documents"][0]