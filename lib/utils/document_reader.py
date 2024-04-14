from lib.utils.constants import DOCUMENT_MAP, INGEST_THREADS
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from langchain.docstore.document import Document
import os


class DocumentReader:
    """
    A class that provides methods for reading and processing documents.
    """

    def file_log(self, message):
        """
        Logs the given message to a file and prints it to the console.

        Args:
            message (str): The message to be logged.
        """
        file1 = open("lib\log_document\document_process_log.txt", "a")
        file1.write(message + "\n")
        file1.close()
        print(message + "\n")

    def load_single_document(self, file_path: str):
        """
        Loads a single document from the given file path.

        Args:
            file_path (str): The path to the document file.

        Returns:
            Document: The loaded document.

        Raises:
            ValueError: If the document type is undefined.
            Exception: If the document fails to load.
        """
        try:
            file_extension = os.path.splitext(file_path)[1]
            loader_class = DOCUMENT_MAP.get(file_extension)
            if loader_class:
                self.file_log(file_path + " loaded.")

                if loader_class.__name__ == "TextLoader":
                    loader = loader_class(file_path=".\\" + file_path, autodetect_encoding=True)
                elif loader_class.__name__ == "CSVLoader":
                    loader = loader_class(file_path=".\\" + file_path, autodetect_encoding=True)
                elif loader_class.__name__ == "UnstructuredPDFLoader":
                    loader = loader_class(file_path=".\\" + file_path)
                elif loader_class.__name__ == "Docx2txtLoader":
                    loader = loader_class(file_path=".\\" + file_path)
            else:
                self.file_log(file_path + " document type is undefined.")
                raise ValueError("Document type is undefined")
            return loader.load()[0]

        except Exception as e:
            self.file_log(file_path + " failed to load.")
            raise e

    def load_document_batch(self, filepaths):
        """
        Loads a batch of documents from a list of file paths.

        Args:
            filepaths (list[str]): The list of file paths.

        Returns:
            tuple: A tuple containing the loaded documents and their file paths.

        Raises:
            ValueError: If the document fails to submit.
        """
        with ThreadPoolExecutor(len(filepaths)) as executor:
            futures = [executor.submit(self.load_single_document, name) for name in filepaths]
            if futures is None:
                self.file_log(self.name + " failed to submit")
                return None
            else:
                data_list = [future.result() for future in futures]
                return (data_list, filepaths)

    def load_documents(self, source_dir: str) -> list[Document]:
        """
        Loads all documents from the source documents directory, including nested folders.

        Args:
            source_dir (str): The path to the source documents directory.

        Returns:
            list[Document]: The list of loaded documents.
        """
        paths = []
        for root, _, files in os.walk(source_dir):
            for file_name in files:
                print("Importing: " + file_name)
                file_extension = os.path.splitext(file_name)[1]
                print("File Extension: " + file_extension)
                source_file_path = os.path.join(root, file_name)
                if file_extension in DOCUMENT_MAP.keys():
                    paths.append(source_file_path)

        n_workers = min(INGEST_THREADS, max(len(paths), 1))
        chunksize = round(len(paths) / n_workers)
        docs = []

        print("Chunks: ", chunksize)
        print("Workers: ", n_workers)
        print("Paths: ", len(paths))

        with ProcessPoolExecutor(n_workers) as executor:
            futures = []
            for i in range(0, len(paths), chunksize):
                filepaths = paths[i: (i + chunksize)]
                try:
                    future = executor.submit(self.load_document_batch, filepaths)
                except Exception as ex:
                    self.file_log("executor task failed: %s" % (ex))
                    future = None
                if future is not None:
                    futures.append(future)
            for future in as_completed(futures):
                try:
                    contents, _ = future.result()
                    docs.extend(contents)
                except Exception as ex:
                    self.file_log("Exception: %s" % (ex))

        return docs

    def split_documents(self, documents: list[Document]) -> tuple[list[Document], list[Document]]:
        """
        Splits the given list of documents for the correct Text Splitter.

        Args:
            documents (list[Document]): The list of documents to be split.

        Returns:
            tuple: A tuple containing the text documents.

        Raises:
            ValueError: If the document type is undefined.
        """
        text_docs = []
        for doc in documents:
            if doc is not None:
                file_extension = os.path.splitext(doc.metadata["source"])[1]
                if file_extension not in DOCUMENT_MAP.keys():
                    raise ValueError("Document type is undefined")
                else:
                    text_docs.append(doc)
        return text_docs