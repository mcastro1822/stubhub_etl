from typing import TypeVar

from pydantic import (
    BaseModel,
    RootModel,
)
from pydantic_mongo import AbstractRepository

T = TypeVar("T", bound=RootModel)
U = TypeVar("U", bound=BaseModel)


def AbstractRepo(model: U, model_set: T, collection: str):
    """
    Creates a abstract repository
    """

    class Repository(AbstractRepository[model]):
        """
        Repository Model
        """

        class Meta:
            collection_name: str = collection

        def get_all(self) -> list[T]:
            """
            Grabs all Items in the MongoDB collection
            """
            return model_set(self.find_by({})).root

    return Repository
