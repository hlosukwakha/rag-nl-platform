import os
import streamlit as st
import httpx

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("RAG NL Platform - Analyst UI")
question = st.text_input("Ask a question about the loaded Dutch datasets")

if st.button("Ask") and question:
    response = httpx.post(f"{API_URL}/ask", json={"question": question, "top_k": 5}, timeout=60)
    payload = response.json()
    st.subheader("Answer")
    st.write(payload["answer"])
    st.subheader("Contexts")
    st.json(payload["contexts"])
