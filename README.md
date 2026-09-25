# RAG Infrastructure

Local integration composition for the RAG stack.

The application repositories own their service Compose definitions. This repository uses Compose `include` rather than duplicating those service definitions.

Expected sibling layout:

    rag-infra/
    rag-ingestion/
    rag-indexer/
    rag-retrieval/
    rag-gateway/

Run:

    docker compose up --build

PostgreSQL is authoritative. Qdrant is a rebuildable search index. Production image pinning and registry publication are intentionally separated into Part 2.
