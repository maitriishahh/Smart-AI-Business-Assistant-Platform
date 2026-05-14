from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

def create_chunks(text:str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                              chunk_overlap=20)
    chunks = splitter.split_text(text)
    return chunks