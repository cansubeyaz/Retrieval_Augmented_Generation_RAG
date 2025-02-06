FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501 8000

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.address=0.0.0.0 --server.port=8501"]