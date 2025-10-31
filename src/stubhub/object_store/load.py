"""
Manages Data Load into object store
"""

import tempfile as tf

import polars as pl
from prefect import task

from stubhub.blocks import blocks


@task(description="Moves to Hetzner Object Store")
async def load_to_object_store(df: pl.DataFrame, landing_path: str):
    """
    Loads to Object store for staging

    Args:
        df: incoming dataframe
    """

    with tf.SpooledTemporaryFile() as temp:

        df.write_parquet(temp)

        temp.seek(0)

        await blocks.object_store.aupload_from_file_object(
            temp,
            landing_path,
        )
