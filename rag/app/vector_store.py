from itertools import zip_longest
from pathlib import Path
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from models import get_gpt_embedding, get_hg_embeddings
from loaders import LoaderRegistry
from splitters import SplitterRegistry
from urllib.parse import urlparse

def qdrant_vector_store(location: str = ":memory:", collection_name: str = "test", embeddings: Embeddings = get_hg_embeddings()):
    client = QdrantClient(":memory:")
    vector_size = len(embeddings.embed_query("sample text"))

    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )

    return QdrantVectorStore( client=client, collection_name=collection_name,
        embedding=embeddings,
    )


class QuerableMemory:
    def __init__(self, vector_store: VectorStore, loader_registry: LoaderRegistry, splitter_registry: SplitterRegistry) -> None:
        self.store = vector_store
        self.loader_registry = loader_registry
        self.splitter_registry = splitter_registry

        self._INGESTION_STRATEGY = {
            "web": ("web", ["recursive"]),
            ".pdf": ("pdf", ["markdown", "recursive"]),
            ".md": ("txt", ["markdown", "recursive"]),
            ".txt": ("txt", ["recursive"])
        }       

    def ingest(self, path: str, loader_type: str, splitter_types: list[str], loader_params={}, splitter_params: list[dict]=[]) -> None:
        """
        It is recommended to use the auto_ingest method instead unless you need fine grained control over loader and splitters.
        """
        loader = self.loader_registry.get(loader_type, path, **loader_params)
        documents = loader.load()
        for stype, params in zip_longest(splitter_types, splitter_params):
            splitter = self.splitter_registry.get(stype, **(params or {}))
            documents = splitter.split_documents(documents)

        self.store.add_documents(documents)

    def auto_ingest(self, path: str, loader_params={}, splitter_params: list[dict]=[]) -> None:
        """
        Loades and splits documents based on the predefined ingestion strategy, then adds them to the vector store.
        """
        if path.startswith(("http://", "https://")):
            key = "web"
        else:
            key = Path(path).suffix

        strategy = self._INGESTION_STRATEGY.get(key)

        if not strategy:
            raise ValueError(f"Unsupported file type or protocol: {key}")

        loader_type, splitter_types = strategy

        return self.ingest(
                    path=path,
                    loader_type=loader_type,
                    splitter_types=splitter_types,
                    loader_params=loader_params,
                    splitter_params=splitter_params
                )

    def retrieve(self, query: str, number_of_documents: int = 4) -> tuple[str, list[Document]]:
        retrieved_docs = self.store.similarity_search(query, number_of_documents)
        serialized = "\n\n".join(
            (f"Source: {doc.metadata}\nContent: {doc.page_content}")
            for doc in retrieved_docs
        )
        return serialized, retrieved_docs