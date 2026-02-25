from langchain_text_splitters import RecursiveCharacterTextSplitter, TextSplitter, MarkdownTextSplitter


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

def default_markdown_text_splitter(**kwargs) -> MarkdownTextSplitter:
    default_headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
    ]

    headers_to_split_on = kwargs.pop("headers_to_split_on", default_headers_to_split_on)

    return MarkdownTextSplitter(headers_to_split_on=headers_to_split_on, **kwargs)

class SplitterRegistry:
    _REGISTRY = {
        "resursive": default_recursive_text_splitter,
    }

    def get(self, type: str, **kwargs) -> TextSplitter:
        func = self._REGISTRY[type]
        if not func:
            raise ValueError(f"Text splitter type of {type} not recoginzed")
        return func(**kwargs)

