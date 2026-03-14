FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY apps/api /app/apps/api
COPY scripts /app/scripts
COPY configs /app/configs
COPY data /app/data
ENV PYTHONPATH=/app
CMD ["uvicorn", "apps.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
