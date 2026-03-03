from pathlib import Path, PurePath
from typing import Sequence
from bs4.filter import SoupStrainer
from langchain_core.document_loaders import BaseLoader
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from langchain_community.document_loaders import WebBaseLoader, TextLoader


def default_pdf_loader(path: str | PurePath, **kwargs) -> PyMuPDF4LLMLoader:
    return PyMuPDF4LLMLoader(file_path=path, **kwargs)

def default_web_loader(path: str | Sequence[str], **kwargs) -> WebBaseLoader:
    default_strainer = SoupStrainer(class_=("post-title", "post-header", "post-content"))
    
    bs_kwargs = kwargs.pop("bs_kwargs", {"parse_only": default_strainer})

    return WebBaseLoader(
        web_path=path,
        bs_kwargs=bs_kwargs,
        **kwargs
    )

def default_text_loader(path: str | Path, **kwargs) -> TextLoader:
    return TextLoader(path, **kwargs)

class LoaderRegistry:
    _REGISTRY = {
        "pdf": default_pdf_loader,
        "web": default_web_loader,
        "txt": default_text_loader
    }

    def get(self, type: str, path: str, **kwargs) -> BaseLoader:
        func = self._REGISTRY[type]
        if not func:
            raise ValueError(f"Loader type of {type} not reconginzed")

        return func(path, **kwargs)