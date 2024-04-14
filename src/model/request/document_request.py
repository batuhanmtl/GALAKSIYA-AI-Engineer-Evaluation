from pydantic import BaseModel, Base64Bytes


from lib.utils.enums import DocumentType

class DocumentRequest(BaseModel):
    base64: Base64Bytes
    filename: str
    filetype: DocumentType