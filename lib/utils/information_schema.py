from typing import Optional

from langchain_core.pydantic_v1 import BaseModel, Field


class Person(BaseModel):
    """
    Represents a person with various attributes.

    Attributes:
        name (Optional[str]): The name of the person.
        about (Optional[str]): The person's writing about herself/himself in the text.
        skills (Optional[list]): The skills of the person, as a list of strings.
        experience (Optional[list]): The experience of the person, as a list of strings.
        education (Optional[list]): The education of the person (high school, university, etc.), as a list of strings.
        languages (Optional[list]): The languages the person speaks, as a list of strings.
        certificates (Optional[list]): The certificates the person has, as a list of strings.
    """
    name: Optional[str] = Field(..., description="The name of the person")
    
    about: Optional[str] = Field(
        ..., description="The person's writing about herself/himself in the text"
    )
    skills: Optional[list] = Field(
        ..., description="The skills of the person, as a list of strings"
    )
    experience: Optional[list] = Field(
        ..., description="The experience of the person, as a list of strings"
    )
    education: Optional[list] = Field(
        ..., description="The education of the person (high school, university, etc.), as a list of strings"
    )
    languages: Optional[list] = Field(
        ..., description="The languages the person speaks, as a list of strings"
    )
    certificates: Optional[list] = Field(
        ..., description="The certificates the person has, as a list of strings"
    )