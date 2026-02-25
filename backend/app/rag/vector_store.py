from itertools import zip_longest
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from app.genai.models import get_gpt_embedding
from app.rag.loaders import LoaderRegistry
from app.rag.splitters import SplitterRegistry
from urllib.parse import urlparse

def qdrant_vector_store(location: str = ":memory:", collection_name: str = "test", embeddings: Embeddings = get_gpt_embedding()):
    client = QdrantClient(":memory:")
    vector_size = len(embeddings.embed_query("sample text"))

    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )

    return QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embeddings,
    )


class QuerableMemory:
    def __init__(self, vector_store: VectorStore, loader_registry: LoaderRegistry, splitter_registry: SplitterRegistry) -> None:
        self.store = vector_store
        self.loader_registry = loader_registry
        self.splitter_registry = splitter_registry

        self._INGESTION_STRATEGY = {
            "web": ("web", ["resursive"]),
            ".pdf": ("pdf", ["markdown", "resursive"]),
            ".md": ("txt", ["markdown", "resursive"]),
            ".txt": ("txt", ["recursive"])
        }       

    def ingest(self, path: str, loader_type: str, splitter_types: list[str], loader_params={}, splitter_params: list[dict]=[]) -> None:
        loader = self.loader_registry.get(loader_type, path, **loader_params)
        documents = loader.load()
        for stype, params in zip_longest(splitter_types, splitter_params):
            splitter = self.splitter_registry.get(stype, **(params | {}))
            documents = splitter.split_documents(documents)

        self.store.add_documents(documents)

    def auto_ingest(self, path: str, loader_params={}, splitter_params={}) -> None:
        ...




