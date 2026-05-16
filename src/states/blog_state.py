from typing import TypedDict
from pydantic import BaseModel, Field


class Blog(BaseModel):
    title: str = Field(description="Title of the Blog")
    content: str = Field(description="Content of Blog post")


class BlogState(TypedDict):
    topic: str
    blog: Blog
    language: str
