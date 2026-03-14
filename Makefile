up:
	docker compose up -d postgres qdrant opensearch elasticsearch weaviate api streamlit nextjs

build:
	docker compose build

ingest:
	docker compose run --rm api python scripts/bootstrap_ingest.py

down:
	docker compose down
