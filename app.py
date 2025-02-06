
import uvicorn
import threading
from app.api import app
from app.streamlit_app import run_streamlit_app

def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    threading.Thread(target=run_api, daemon=True).start()
    run_streamlit_app()



