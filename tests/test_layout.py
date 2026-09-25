from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_compose_includes_all_service_repositories_without_overrides():
    compose = (ROOT / "compose.yaml").read_text()

    assert "../rag-ingestion/docker-compose.yml" in compose
    for repo in ("rag-indexer", "rag-retrieval", "rag-gateway"):
        assert f"../{repo}/compose.yaml" in compose

    # Included application services are owned by their repositories. Redefining
    # them here causes Docker Compose include conflicts and duplicates ownership.
    assert "  pst-agent:" not in compose
    assert "  rag-indexer:" not in compose
    assert "  rag-retrieval:" not in compose
    assert "  rag-gateway:" not in compose


def test_qdrant_is_version_pinned_and_persistent():
    compose = (ROOT / "compose.yaml").read_text()

    assert "qdrant/qdrant:v1.19.1" in compose
    assert "qdrant-data:/qdrant/storage" in compose
    assert "6333:6333" in compose
    assert "6334:6334" in compose


def test_environment_has_no_default_secret():
    env = (ROOT / ".env.example").read_text()

    assert "replace-with-a-long-random-secret" in env
    assert "replace-me" not in env
