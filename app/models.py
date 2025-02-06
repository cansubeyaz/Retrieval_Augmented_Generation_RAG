
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import faiss
import PyPDF2
import docx
import io
from fastapi import HTTPException
from .config import Settings
import os

class RAGPipeline:
    def __init__(self, openai_api_key=None):
        self.embedding_model = SentenceTransformer(Settings.EMBEDDING_MODEL)
        self.index = faiss.IndexFlatL2(Settings.VECTOR_DIMENSION)
        self.documents = []
        self.document_sources = []
        self.client = OpenAI(api_key=openai_api_key) if openai_api_key else None

    def reset_index(self):
        self.index = faiss.IndexFlatL2(Settings.VECTOR_DIMENSION)
        self.documents = []
        self.document_sources = []

    def process_document(self, file_name: str, file_content: bytes):
        file_ext = os.path.splitext(file_name)[1].lower()
        text = ""

        try:
            if file_ext == ".pdf":
                text = self._process_pdf(file_content)
            elif file_ext == ".docx":
                text = self._process_docx(file_content)
            elif file_ext == ".txt":
                text = file_content.decode("utf-8")
            else:
                raise ValueError(f"Unsupported file type: {file_ext}")

            chunks = []
            for i in range(0, len(text), Settings.CHUNK_SIZE - Settings.CHUNK_OVERLAP):
                chunks.append(text[i:i+Settings.CHUNK_SIZE])

            if chunks:
                embeddings = self.embedding_model.encode(chunks)
                self.index.add(embeddings)
                self.documents.extend(chunks)
                self.document_sources.extend([file_name] * len(chunks))
                return len(chunks)
            return 0
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing document: {e}")

    def _process_pdf(self, file_content: bytes):
        try:
            with io.BytesIO(file_content) as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                text = "".join(page.extract_text() + "\n" for page in pdf_reader.pages if page.extract_text())
            return text
        except Exception as e:
            raise ValueError(f"Failed to process PDF: {e}")
    
    def _process_docx(self, file_content: bytes):
        try:
            with io.BytesIO(file_content) as docx_file:
                doc = docx.Document(docx_file)
                return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            raise ValueError(f"Failed to process DOCX: {e}")

    def search(self, query, top_k=5):
        if self.index.ntotal == 0:
            return [], []
        query_embedding = self.embedding_model.encode([query])
        D, I = self.index.search(query_embedding, top_k)
        return [self.documents[idx] for idx in I[0]], [self.document_sources[idx] for idx in I[0]]

    def generate_answer(self, query, retrieved_docs):
        context = " ".join(retrieved_docs)
        if not self.client:
            return "OpenAI client not initialized."

        try:
            chat_completion = self.client.chat.completions.create(
                model=Settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."}, #I am leaving like this but i can recommend that you should update this part according to your documents
                    {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
                ],
                max_tokens=Settings.MAX_TOKENS
            )
            return chat_completion.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating answer: {str(e)}"