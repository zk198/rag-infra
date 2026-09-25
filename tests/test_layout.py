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


def test_only_gateway_is_host_exposed_application_service():
    service_compose = {
        "rag-ingestion": ROOT.parent / "rag-ingestion" / "docker-compose.yml",
        "rag-indexer": ROOT.parent / "rag-indexer" / "compose.yaml",
        "rag-retrieval": ROOT.parent / "rag-retrieval" / "compose.yaml",
        "rag-gateway": ROOT.parent / "rag-gateway" / "compose.yaml",
    }

    # These sibling repositories are checked out by the integration CI job.
    # Keep the test useful for local pytest runs where they may be absent.
    available = {name: path for name, path in service_compose.items() if path.exists()}
    if not available:
        return

    for name in ("rag-ingestion", "rag-indexer", "rag-retrieval"):
        path = service_compose[name]
        if path.exists():
            compose = path.read_text()
            assert "\n    ports:" not in compose, f"{name} must remain internal"

    gateway = service_compose["rag-gateway"]
    if gateway.exists():
        compose = gateway.read_text()
        assert '      - "8000:8200"' in compose
