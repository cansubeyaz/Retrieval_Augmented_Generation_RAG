import os

class Settings:
    EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
    VECTOR_DIMENSION = 384
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 100
    MAX_TOKENS = 300
    OPENAI_MODEL = "gpt-4o-mini"  # In my case only 4o-mini works thats why I dont recommend to change
