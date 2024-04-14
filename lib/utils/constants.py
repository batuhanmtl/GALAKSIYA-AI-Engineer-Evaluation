import os
from langchain_community.document_loaders import TextLoader, UnstructuredPDFLoader,Docx2txtLoader


# find SOURCE_DOCUMENTS path
SOURCE_DIRECTORY = "lib\SOURCE_DOCUMENTS"

PERSIST_DIRECTORY = "lib\VECTOR_DB"

DOCUMENT_MAP = {
    ".txt" : TextLoader,
    ".pdf" : UnstructuredPDFLoader,
    ".docx": Docx2txtLoader
}

# Can be changed to a specific number
INGEST_THREADS = os.cpu_count() or 8

