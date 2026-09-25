from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_compose_includes_all_service_repositories():
    compose = (ROOT / "compose.yaml").read_text()

    for repo in (
        "rag-ingestion",
        "rag-indexer",
        "rag-retrieval",
        "rag-gateway",
    ):
        assert f"../{repo}/compose.yaml" in compose


def test_qdrant_is_version_pinned_and_persistent():
    compose = (ROOT / "compose.yaml").read_text()

    assert "qdrant/qdrant:v1.19.1" in compose
    assert "qdrant-data:/qdrant/storage" in compose
    assert "6333:6333" in compose
    assert "6334:6334" in compose


def test_only_gateway_is_host_exposed_for_application_traffic():
    compose = (ROOT / "compose.yaml").read_text()

    assert '  rag-gateway:
    ports:
      - "8000:8000"' in compose
    assert "  rag-retrieval:
    ports: []" in compose
    assert "  pst-agent:
    ports: []" in compose


def test_environment_has_no_default_secret():
    env = (ROOT / ".env.example").read_text()

    assert "replace-with-a-long-random-secret" in env
    assert "replace-me" not in env
