FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir streamlit httpx
COPY apps/streamlit-ui /app/apps/streamlit-ui
CMD ["streamlit", "run", "apps/streamlit-ui/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
