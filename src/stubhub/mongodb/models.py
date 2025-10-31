"""
Creates MongoDB Document Models
"""

from pydantic import BaseModel, Field, RootModel
from pydantic_mongo import ObjectIdAnnotation

from stubhub.mongodb.db import AbstractRepo


class Query(BaseModel):
    """
    URL Query Model Params
    """

    id: ObjectIdAnnotation = Field(exclude=True)
    stubhub_name: str
    stubhub_id: int


class QueryModel(RootModel):
    """
    Root Model
    """

    root: list[Query]


class StubhubRepo(AbstractRepo(Query, QueryModel, "product_stubhub")):
    """
    Model for MongoDB Interaction
    """

    ...
