from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import LLMMathChain
from langchain_openai import OpenAI, ChatOpenAI
from lib.utils.information_schema import Person
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from lib.utils.base64_to_text import Base64ToText
from langchain_core.messages import HumanMessage
from lib.utils.constants import PERSIST_DIRECTORY
from lib.utils.log_qa import (
    similarity_log_qa,
    math_solver_log_qa,
    text_to_pdf_similarity_qa,
    text_to_pdf_math_solver_qa,
    data_extractor_log_qa,
    text_to_data_extractor_qa,
)
from src.model.request.document_request import DocumentRequest

class LLMService:
    """
    A class that provides various services using the LLM (Language Model) API.

    Attributes:
        embeddings (OpenAIEmbeddings): An instance of the OpenAIEmbeddings class.
        llm (OpenAI): An instance of the OpenAI class for language generation.
        llm_math (LLMMathChain): An instance of the LLMMathChain class for math solving.
        person (Person): An instance of the Person class for data extraction.
        chat (ChatOpenAI): An instance of the ChatOpenAI class for chat-based language generation.
        base64_to_text (Base64ToText): An instance of the Base64ToText class for base64 decoding.
    """

    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.llm = OpenAI(temperature=0, model_name="gpt-3.5-turbo-instruct")
        self.llm_math = LLMMathChain.from_llm(self.llm, verbose=True)
        self.person = Person
        self.chat = ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0)
        self.base64_to_text = Base64ToText

    def similarity_search(self, query: str):
        """
        Performs a similarity search based on the given query.

        Args:
            query (str): The query string for similarity search.

        Returns:
            list: List of documents similar to the query with their sources.
        """
        vector_store = FAISS.load_local(
            index_name="openai_index",
            folder_path=PERSIST_DIRECTORY,
            embeddings=self.embeddings,
            allow_dangerous_deserialization=True,
            normalize_L2=True,
        )

        docs = vector_store.similarity_search_with_score(query, k=2)

        similarity_log_qa(input=query, output=docs)
        text_to_pdf_similarity_qa()

        return [
            {
                "source": doc.metadata["source"],
                "content": doc.page_content,
                "similarity_L2_score": float(score),
            }
            for doc, score in docs
        ]

    def math_solver(self, query: str):
        """
        Solves a math problem based on the given query.

        Args:
            query (str): The math problem to be solved.

        Returns:
            str: The solution to the math problem.
        """

        result = self.llm_math.invoke(query)
        result = result["answer"]
        result = result.split("Answer: ")[1]

        math_solver_log_qa(input=query, output=result)
        text_to_pdf_math_solver_qa()

        return result

    def data_extractor(self, document: DocumentRequest):
        """
        Extracts relevant information from a document based on the given base64 string, filename, and filetype.

        Args:
            base64 (str): The base64 encoded string of the document.
            filename (str): The name of the document.
            filetype (str): The type of the document.

        Returns:
            dict: A dictionary containing the extracted information.
        """
        doc_str = self.base64_to_text.get_doc(document.base64, document.filetype.value)

        example = """{
            "name": "John Doe",
            "about": "I am a software engineer with 5 years of experience in web development.",
            "skills": ["Python", "JavaScript", "React"],
            "experience": ["Software Engineer at Company A", "Web Developer at Company B"],
            "education": ["Bachelor's in Computer Science at University A", "Master's in Software Engineering at University B"],
            "languages": ["English", "Spanish"],
            "certificates": ["Certificate in Web Development", "Certificate in Data Science"]
        }"""

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an expert extraction algorithm. "
                    "Only extract relevant information from the resume. "
                    "If you do not know the value of an attribute asked to extract, "
                    "return null for the attribute's value.",
                ),
                # Please see the how-to about improving performance with
                # reference examples.
                MessagesPlaceholder("examples"),
                ("user", "{text}"),
            ]
        )

        llm = self.chat

        runnable = prompt | llm.with_structured_output(schema=Person, include_raw=False)

        response = runnable.invoke(
            {"text": doc_str, "examples": [HumanMessage(content=example)]}
        )

        data_extractor_log_qa(document.filename, document.filetype.value, response)
        text_to_data_extractor_qa()

        return response
