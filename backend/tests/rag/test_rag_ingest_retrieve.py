from pathlib import Path
from langchain_core.documents import Document
import pytest

from app.rag import vector_store
from app.rag.loaders import LoaderRegistry
from app.rag.splitters import SplitterRegistry
from app.rag.vector_store import QuerableMemory, qdrant_vector_store

def get_all_documents(vec_store):
    """
    Returns every document in the store as a list of LangChain Document objects.
    """
    results, _ = vec_store.client.scroll(
        collection_name=vec_store.collection_name,
        limit=1000
    )
    
    return [
        Document(
            page_content=p.payload["page_content"], 
            metadata=p.payload["metadata"]
        ) for p in results
    ]

def test_auto_ingest_markdown():
    vec_store = qdrant_vector_store()
    loader_reg = LoaderRegistry()
    splitter_reg = SplitterRegistry()
    memory = QuerableMemory(vec_store, loader_reg, splitter_reg)

    current_dir = Path(__file__).parent
    md_path = str(current_dir / "data" / "example_rule_book.md")

    # with open(md_path, "r", encoding="utf-8") as f:
    #     original_content = f.read()
    
    memory.auto_ingest(md_path)

    # Debug Printing
    all_docs = get_all_documents(vec_store)
    print("\n" + " COMPOSITION MAP ".center(75, "="))
    print(f"{'INDEX':<6} | {'HEADERS BREADCRUMB':<45} | {'SIZE':<10}")
    print("-" * 75)
    
    for i, doc in enumerate(all_docs):
        h1 = doc.metadata.get("Header 1", "Root")
        h2 = doc.metadata.get("Header 2", "")
        h3 = doc.metadata.get("Header 3", "")
        
        parts = [h1[:12].strip()]
        if h2: 
            parts.append(h2[:12].strip())
        if h3: 
            parts.append(h3[:12].strip())
        
        breadcrumb = " > ".join(parts)
        
        size = len(doc.page_content)
        print(f"{i:<6} | {breadcrumb:<45} | {size:<8} chars")
    print("=" * 75 + "\n")

    query = "hostile metal spider"
    res = vec_store.similarity_search(query, k=1)
    
    assert len(res) > 0, "Vector store returned no results."
    doc = res[0]

    assert "##" not in doc.page_content
    assert "hostile metal spider" in doc.page_content

    assert doc.metadata["Header 1"] == "🌑 DUST & DROSS: A Pocket RPG"
    assert doc.metadata["Header 2"] == "🎲 Core Mechanics"
    
    assert doc.metadata["source"] == str(md_path)

