
from fastapi import FastAPI, UploadFile, File
from .models import RAGPipeline

app = FastAPI()
rag_pipeline = RAGPipeline()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/documents/process")
def process_document(file: UploadFile = File(...)):
    file_content = file.file.read()
    processed_chunks = rag_pipeline.process_document(file.filename, file_content)
    return {"message": f"Processed {processed_chunks} chunks", "filename": file.filename}

@app.get("/search")
def search_documents(query: str, top_k: int = 5):
    docs, sources = rag_pipeline.search(query, top_k)
    if not docs:
        return {"message": "No relevant documents found"}
    return {"documents": docs, "sources": sources}
