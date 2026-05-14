from backend.app.rag.document_loader import load_pdf

from backend.app.rag.chunking import create_chunks

from backend.app.rag.embeddings import generate_embeddings

async def process_upload_document(file_path: str, user_id:str, filename:str):
    text = load_pdf(file_path)
    chunks = create_chunks(text)

    await generate_embeddings(
        chunks=chunks,
        user_id=user_id,
        filename=filename
    )