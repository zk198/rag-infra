from pathlib import Path

def test_compose_includes_service_owned_definitions():
    compose=(Path(__file__).parents[1]/"compose.yaml").read_text()
    for name in ("rag-ingestion","rag-indexer","rag-retrieval","rag-gateway"):
        assert f"../{name}/compose.yaml" in compose
