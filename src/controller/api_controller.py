from fastapi_restful.cbv import cbv
from fastapi import APIRouter, Depends

from src.model.request.query_request import QueryRequest
from src.model.request.document_request import DocumentRequest

from src.service.llm_service import LLMService


router = APIRouter(prefix="/api/v1", tags=["Api Controller"])


@cbv(router)
class ApiController:
    """
    Controller class for API endpoints.
    """

    def __init__(self, llm_service: LLMService = Depends()):
        """
        Constructor method for ApiController.

        Args:
            llm_service (LLMService, optional): Instance of LLMService. Defaults to Depends().
        """
        self.llm_service = llm_service

    @router.post("/similarity_search")
    async def similarity_search(self, request: QueryRequest):
        """
        Endpoint for performing similarity search.
        Args:
            request (QueryRequest): Query request object contains query string.
        Returns:
            response (List): Best 3 documents that are similar to the query.

        Example:
            input: {
                "query": "sorgu cümlesi"
            }
            output: [
            {
                "source": ".\\lib\\SOURCE_DOCUMENTS\\ilgili_doküman.(pdf,docx,txt)",
                "content": "Query'e yanıt içermesi muhtemel olan dokümandaki kısmın içeriği",
                "similarity_L2_score": 0.20954060554504395 
            }
            ]


        """
        return self.llm_service.similarity_search(request.query)

    @router.post("/math_solver")
    async def math_solver(self, request: QueryRequest):
        """
        Endpoint for solving math problems.

        Args:
            request (QueryRequest): Query request object contains query string.

        Returns:
            str : The solution to the basic math problem.

            Example:
            input: {
                "query": "two plus two"
            }
            output: "4"
        """
        return self.llm_service.math_solver(request.query)

    @router.post("/data_extractor")
    async def data_extractor(self, document: DocumentRequest):
        """
        Endpoint for extracting data from resume.

        Args:
            document (DocumentRequest): Document request object contains document details.

        Returns:
            dict: Extracted data from the document.

            Example:
            input: {
                "base64": "base64 string",
                "filename": "document.pdf",
                "filetype": "pdf"
            }
            output: {
                "name": "John Doe",
                "about": "I am a software engineer.",
                "skills": ["Python", "Java", "C++"],
                "experience": ["Software Engineer at Company A"],
                "education": ["Bachelor's Degree in Computer Science"],
                "languages": ["English", "Spanish"],
                "certificates": ["Certificate in Python Programming"]
            }
        """
        print("Data extractor is called.")

        base64 = document.base64
        filename = document.filename
        filetype = document.filetype.value
        # print(filename, filetype)
        return self.llm_service.data_extractor(base64, filename, filetype.lower())

