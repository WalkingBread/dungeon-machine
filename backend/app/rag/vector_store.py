from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient



# In memory for testing purposes
client = QdrantClient(":memory:")

vector_size = len(embededdings.embed_query("sample text"))



