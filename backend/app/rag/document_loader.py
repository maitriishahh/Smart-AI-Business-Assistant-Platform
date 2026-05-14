from langchain_community.document_loaders import PyPDFLoader

def load_pdf(file_path:str):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    text = "\n".join([doc.page_content for doc in documents])
    return text