from abc import ABC, abstractmethod
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter, TextSplitter, MarkdownHeaderTextSplitter

class MarkdownHeaderWrapper:
    def __init__(self, splitter: MarkdownHeaderTextSplitter):
        self.splitter = splitter

    def split_documents(self, documents: list[Document]) -> list[Document]:
        output = []
        for doc in documents:
            # Split the text and merge the original metadata (source, etc.)
            chunks = self.splitter.split_text(doc.page_content)
            for chunk in chunks:
                chunk.metadata = {**doc.metadata, **chunk.metadata}
                output.append(chunk)
        return output


def default_recursive_text_splitter(**kwargs) -> RecursiveCharacterTextSplitter:
    chunk_size = kwargs.pop("chunk_size", 5000)
    chunk_overlap = kwargs.pop("chunk_overlap", 500)
    add_start_index = kwargs.pop("add_start_index", True)

    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=add_start_index,
        **kwargs
    )

def default_markdown_text_splitter(**kwargs) -> MarkdownHeaderWrapper:
    default_headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]

    headers_to_split_on = kwargs.pop("headers_to_split_on", default_headers_to_split_on)

    return MarkdownHeaderWrapper(MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on, **kwargs))

class SplitterRegistry:
    _REGISTRY = {
        "recursive": default_recursive_text_splitter,
        "markdown": default_markdown_text_splitter,
    }

    def get(self, type: str, **kwargs) -> TextSplitter:
        func = self._REGISTRY[type]
        if not func:
            raise ValueError(f"Text splitter type of {type} not recoginzed")
        return func(**kwargs)