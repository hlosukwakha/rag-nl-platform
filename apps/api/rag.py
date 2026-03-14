from __future__ import annotations

import os
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, PointStruct, VectorParams
from sentence_transformers import SentenceTransformer


class RAGService:
    def __init__(self) -> None:
        model_name = os.getenv(
            "EMBEDDING_MODEL",
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        )
        self.embedder = SentenceTransformer(model_name)
        self.qdrant = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))
        self.collection = "nl_open_data"
        self._ensure_collection()

    def _ensure_collection(self) -> None:
        try:
            self.qdrant.get_collection(self.collection)
        except Exception:
            dim = len(self.embedder.encode(["hello"])[0])
            self.qdrant.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
            )

    def list_sources(self) -> dict[str, Any]:
        return {
            "collection": self.collection,
            "vector_backend": "qdrant",
            "configured_models": [
                "LLaMA",
                "Mistral",
                "Phi-2",
                "DeepSeek",
                "Qwen",
                "Gemma",
            ],
            "frameworks": [
                "LangChain",
                "Haystack",
                "CrewAI",
                "HuggingFace",
                "LlamaIndex",
            ],
        }

    def index_documents(self, docs: list[dict[str, Any]]) -> None:
        if not docs:
            return
        vectors = self.embedder.encode([d["text"] for d in docs]).tolist()
        points = [
            PointStruct(id=i, vector=vectors[i], payload=docs[i])
            for i in range(len(docs))
        ]
        self.qdrant.upsert(collection_name=self.collection, points=points)

    def answer(self, question: str, top_k: int = 5) -> dict[str, Any]:
        qv = self.embedder.encode(question).tolist()
        hits = self.qdrant.search(
            collection_name=self.collection,
            query_vector=qv,
            limit=top_k,
        )
        contexts = [h.payload for h in hits]
        answer = self._synthesise(question, contexts)
        return {
            "question": question,
            "answer": answer,
            "contexts": contexts,
        }

    def _synthesise(self, question: str, contexts: list[dict[str, Any]]) -> str:
        if not contexts:
            return "No indexed context found yet. Run the bootstrap ingest first."

        lines = [f"Question: {question}", "Relevant context:"]
        for c in contexts[:5]:
            source = c.get("source", "unknown")
            title = c.get("title", "untitled")
            text = c.get("text", "")
            lines.append(f"- [{source}] {title}: {text[:300]}")

        lines.append(
            "This starter project returns a grounded retrieval summary. "
            "Replace this synthesiser with a local open-source chat model call "
            "via Hugging Face TGI, vLLM, Ollama, or Haystack generators."
        )
        return "\n".join(lines)
