# Retrieval-Augmented Generation (RAG) System

## Overview

This project implements a Retrieval-Augmented Generation (RAG) system that processes, indexes, and retrieves knowledge from documents using Sentence Transformers for embeddings and FAISS for efficient vector search. An LLM (OpenAI GPT) can generate answers based on retrieved content.

![Streamlit Interface](images/streamlit.gif)

## Features

- Support for multiple document formats (PDF, DOCX, TXT)
- Semantic search using sentence transformers
- GPT-powered answer generation
- Dual interface: Web UI (Streamlit) and REST API
- Docker support for easy deployment

## Project Structure
```
rag-pipeline/
├── app/
│   ├── __init__.py
│   ├── api.py
│   ├── config.py
│   ├── models.py
│   └── streamlit_app.py
├── app.py
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```
