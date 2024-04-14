import os
from fastapi import FastAPI
from src.controller.api_controller import router as home_router
from src.config.create_vector_store import CreateVectorStore

class GalaksiyaApplication(FastAPI):
    """
    Represents the Galaksiya Application.

    This class initializes the FastAPI application and provides methods to include routers and run the application.
    """

    def __init__(self):
        """
        Initializes the GALAKSIYA API.

        If the 'lib/VECTOR_DB' folder is empty, a vector store is created.

        Parameters:
            None

        Returns:
            None
        """
        if not os.path.exists("lib/VECTOR_DB/openai_index.faiss") or not os.path.exists("lib/VECTOR_DB/openai_index.pkl"):
            CreateVectorStore()
            
        super().__init__(
            title="GALAKSIYA",
            description="API that serves a tool-based agent",
            summary="AI Engineer Evaluation Case",
            version="v1",
            terms_of_service="http://example.com/terms/",
            contact={
                "url": "https://www.galaksiya.com/",
                "email": "info@galaksiya.com"
            },
            license_info={
                "name": "Apache 2.0",
                "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
            }
        )
        self.include_router(home_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:GalaksiyaApplication", reload=True,factory=True, log_level="info",env_file=".env")
