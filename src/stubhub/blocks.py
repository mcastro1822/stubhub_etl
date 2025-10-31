"""
Blocks used in Zillow ETL
"""

from prefect_aws.s3 import S3Bucket
from prefecto.blocks import lazy_load

from stubhub.mongodb.mongodb import MongoDB


class Blocks:
    """Class for lazy loading Prefect Blocks."""

    # Define the block name variables
    mongo_block: str = "mongodb-prod"
    s3_block: str = "hetzner-stubhub-bucket"

    @property
    @lazy_load("mongo_block")
    def mongodb(self) -> MongoDB:
        """The Mongo block."""

    @property
    @lazy_load("s3_block")
    def object_store(self) -> S3Bucket:
        """The Bucket block."""


blocks = Blocks()
