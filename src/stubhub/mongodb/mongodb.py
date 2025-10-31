"""
authored by Yegor Bryzhan @ybryzTE
Edits made by Michael Castro
"""

from prefect.blocks.core import Block
from pydantic import SecretStr, model_validator
from pymongo import MongoClient


class MongoDB(Block):
    """
    MongoDB access block
    """

    host: str
    username: str | None = None
    password: SecretStr | None = None

    _block_type_name = "MongoDB"

    @model_validator(mode="before")
    def validate_input(cls, values):
        """
        Verifies that a username and password are provided
        """
        if values["username"] is None and values["password"] is None:
            raise ValueError("Username and password must be specifed")
        else:
            return values

    def get_client(self) -> MongoClient:

        return MongoClient(
            host=self.host,
            username=self.username,
            password=self.password.get_secret_value(),
            authSource="production",
        )
