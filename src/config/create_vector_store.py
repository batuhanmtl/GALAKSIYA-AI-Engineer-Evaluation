# encoding:utf-8

import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from lib.utils.constants import SOURCE_DIRECTORY, PERSIST_DIRECTORY
from lib.utils.document_reader import DocumentReader

class CreateVectorStore:
    """
    Class responsible for creating a vector store from a set of documents.
    """

    def __init__(self):
        """
        Initializes the CreateVectorStore object.
        """

        self.reader = DocumentReader() 
        self.embeddings = OpenAIEmbeddings()

        self.source_directory = SOURCE_DIRECTORY
        self.persist_directory = PERSIST_DIRECTORY

        self.documents = self.reader.load_documents(self.source_directory)
        self.text_docs = self.reader.split_documents(self.documents)

        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

        self.text = self.text_splitter.split_documents(self.text_docs)

        logging.info(f"Loaded {len(self.text_docs)} documents from {self.source_directory}")
        logging.info(f"Split into {len(self.text)} chunks of text")

        DocumentReader.file_log(self, f"Loaded {len(self.text_docs)} documents from {self.source_directory}")
        DocumentReader.file_log(self, f"Split into {len(self.text)} chunks of text")

        self.vector_store = FAISS.from_documents(self.text, embedding=self.embeddings, normalize_L2=True)

        self.vector_store.save_local(index_name="openai_index",folder_path=self.persist_directory)





    
        







