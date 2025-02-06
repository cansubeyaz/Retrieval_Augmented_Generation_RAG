import streamlit as st
from .models import RAGPipeline

def run_streamlit_app():
    st.title("RAG Pipeline with OpenAI & REST API")

    if 'retrieved_docs' not in st.session_state:
        st.session_state.retrieved_docs = []
    if 'retrieved_sources' not in st.session_state:
        st.session_state.retrieved_sources = []

    openai_api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

    if 'rag_pipeline' not in st.session_state or st.session_state.api_key != openai_api_key:
        if openai_api_key:
            st.session_state.rag_pipeline = RAGPipeline(openai_api_key=openai_api_key)
            st.session_state.api_key = openai_api_key
        else:
            st.warning("Please enter an OpenAI API Key")
            return

    st.header("Upload Documents")
    uploaded_files = st.file_uploader("Choose documents", type=['pdf', 'docx', 'txt'], accept_multiple_files=True)

    if uploaded_files:
        st.session_state.rag_pipeline.reset_index()
        processed_docs = 0
        for uploaded_file in uploaded_files:
            chunks = st.session_state.rag_pipeline.process_document(uploaded_file.name, uploaded_file.getvalue())
            processed_docs += chunks

        st.success(f"Processed {processed_docs} document chunks across {len(uploaded_files)} files")

    st.header("Search Documents")
    query = st.text_input("Enter your search query:")

    if query:
        st.session_state.retrieved_docs, st.session_state.retrieved_sources = st.session_state.rag_pipeline.search(query)
        
        st.subheader("Retrieved Passages:")
        for i, (doc, source) in enumerate(zip(st.session_state.retrieved_docs, st.session_state.retrieved_sources), 1):
            # Extract filename without extension for nice view
            filename = source.rsplit('.', 1)[0]
            # Calculate approximate word count 
            word_count = len(doc.split())

            chunk_title = f"Passage {i}: {filename} ({word_count} words)"
            
            with st.expander(chunk_title):
                st.text_area("Content", doc, height=100)
                st.caption(f"Source: {source}")
        
        answer = st.session_state.rag_pipeline.generate_answer(query, st.session_state.retrieved_docs)
        
        st.subheader("Generated Answer:")
        st.write(answer)