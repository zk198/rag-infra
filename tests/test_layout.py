from pathlib import Path

def test_service_repositories_are_expected_siblings():
    root=Path(__file__).resolve().parents[1]
    for name in ("rag-ingestion","rag-indexer","rag-retrieval","rag-gateway"):
        assert (root.parent/name).name == name
