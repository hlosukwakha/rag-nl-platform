from __future__ import annotations

import json
import httpx
from apps.api.rag import RAGService

PDOK_EXAMPLE = "https://api.pdok.nl/bzk/locatieserver/search/v3_1/free?q=Alkmaar"


def safe_fetch_json(url: str):
    resp = httpx.get(url, timeout=30, follow_redirects=True)
    resp.raise_for_status()
    data = resp.json()

    if isinstance(data, dict) and "error" in data:
        raise ValueError(f"API returned error payload: {data['error']}")

    return data


def add_doc_if_valid(docs: list[dict], source: str, title: str, data, url: str) -> None:
    text = json.dumps(data, ensure_ascii=False)[:4000]
    lowered = text.lower()

    bad_markers = [
        "403 forbidden",
        "302 found",
        "pagina-niet-gevonden",
        '"error"',
    ]
    if any(marker in lowered for marker in bad_markers):
        return

    docs.append(
        {
            "source": source,
            "title": title,
            "text": text,
            "url": url,
        }
    )


def build_docs() -> list[dict]:
    docs: list[dict] = []

    # Local seed docs first so the RAG has useful population content
    docs.extend(
        [
            {
                "source": "CBS",
                "title": "Netherlands population growth overview",
                "text": (
                    "The population of the Netherlands has grown over time. "
                    "Important drivers include births, deaths, immigration, and emigration. "
                    "In recent years, migration has been a major contributor to population growth."
                ),
                "url": "local-seed",
            },
            {
                "source": "CBS",
                "title": "Population growth drivers",
                "text": (
                    "Population change in the Netherlands is shaped by natural increase "
                    "(births minus deaths) and net migration. Growth is often stronger in "
                    "urban and economically active regions."
                ),
                "url": "local-seed",
            },
        ]
    )

    # Optional live example: PDOK, but only if valid
    try:
        pdok = safe_fetch_json(PDOK_EXAMPLE)
        add_doc_if_valid(
            docs,
            "PDOK",
            "PDOK location lookup Alkmaar",
            pdok,
            PDOK_EXAMPLE,
        )
    except Exception as exc:
        print(f"Skipping PDOK_EXAMPLE: {exc}")

    return docs


def main():
    service = RAGService()
    docs = build_docs()
    service.index_documents(docs)
    print(f"Indexed {len(docs)} documents")


if __name__ == "__main__":
    main()
