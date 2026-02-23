from langchain_core.vectorstores import VectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters.base import TextSplitter
from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_core.document_loaders.base import BaseLoader
from langchain_core.documents import Document

from app.genai.models import get_gpt_embedding

COLLECTION_NAME = "test"

embeddings = get_gpt_embedding()

# In memory for testing purposes
client = QdrantClient(":memory:")
vector_size = len(embeddings.embed_query("sample text"))

# Test collection creation
if not client.collection_exists(COLLECTION_NAME):
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
    )

default_vector_store = QdrantVectorStore(
    client=client,
    collection_name=COLLECTION_NAME,
    embedding=embeddings,
)

default_recursive_text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=5000,
    chunk_overlap=500,
    add_start_index=True,
)

def load_and_split(loader: BaseLoader, splitter: TextSplitter = default_recursive_text_splitter) -> list[Document]:
    docs = loader.load()
    all_splits = splitter.split_documents(docs)
    return all_splits

def store_documents(documents: list[Document], vector_store: VectorStore = default_vector_store) -> list[str]:
    return vector_store.add_documents(documents)


