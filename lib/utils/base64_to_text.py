from lib.utils.constants import DOCUMENT_MAP
from pydantic import Base64Bytes
from lib.utils.document_reader import DocumentReader

import tempfile
import os

TEMP_DIR = tempfile.gettempdir()

file_log = DocumentReader().file_log


class Base64ToText:
    """
    A utility class for decoding base64 strings and extracting text content from different file formats.
    """

    @staticmethod
    def _remove_file_from_tempdir(file_path: str):
        """
        Removes the file from the temporary directory.

        Args:
            file_path (str): The path of the file to be removed.
        """
        os.remove(file_path)
        
    @staticmethod
    def decode(base64_string: Base64Bytes, file_extension: str) -> str:
        """
        Decodes the base64 string and saves it as a file with the specified file extension.

        Args:
            base64_string (str): The base64 encoded string.
            file_extension (str): The file extension of the decoded file.

        Returns:
            tuple: A tuple containing the file path and file extension of the decoded file.
        """
        _file_extension = f".{file_extension}"

        binary_data = base64_string
        file_path = f"{TEMP_DIR}/temp{_file_extension}"
        with open(file_path, "wb") as file:
            file.write(binary_data)
        return file_path, _file_extension

    @staticmethod
    def get_doc(base64_string: Base64Bytes, file_extension: str) -> str:
        """
        Extracts the text content from the decoded resumme file.

        Args:
            base64_string (str): The base64 encoded string.
            file_extension (str): The file extension of the decoded file.

        Returns:
            str: The extracted text content from the file.

        Raises:
            Exception: If the file format is not supported.
        """
        try:
            path, _file_extension = Base64ToText.decode(base64_string, file_extension)

            loader = DOCUMENT_MAP.get(_file_extension)

            if loader.__name__ == "TextLoader":
                    loader = loader(file_path=path, autodetect_encoding=True)
            elif loader.__name__ == "CSVLoader":
                loader = loader(file_path=path, autodetect_encoding=True)
            elif loader.__name__ == "UnstructuredPDFLoader":
                loader = loader(file_path=path)
            elif loader.__name__ == "Docx2txtLoader":
                loader = loader(file_path=path)

            else:
                file_log(path + " document type is undefined.")
                raise ValueError("Document type is undefined")
            
                      
            
            doc_str = loader.load()[0].page_content

            Base64ToText._remove_file_from_tempdir(path)
            
            return doc_str
        
        except Exception as e:
            print(f"Error: {e}")
            return None
        


