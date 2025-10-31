"""
Handles Lake Path Creation
"""

from enum import StrEnum
from pathlib import Path

import pendulum as pd


class Status(StrEnum):

    failed = "failed"
    loaded = "loaded"
    staged = "staged"


class LakePath:

    def __init__(self):

        self.root: Path = Path("")

    def dataset(self, dataset):
        """
        Adds dataset type to path
        """

        self.root = self.root / f"dataset={dataset}"

        return self

    def id(self, id):
        """
        Adds identifier subfolder
        """

        self.root = self.root / f"id={id}"

        return self

    def extract_date(self, extract_date):
        """
        Adds extract date subfolder
        """

        self.root = self.root / f"extract-date={extract_date}"

        return self

    def status(self, status):
        """
        Adds status date subfolder
        """

        self.root = self.root / f"status={status}"

        return self

    def join(self, item):

        self.root = self.root / item

        return self

    def render(self):
        return self.root.as_posix()


def staging_path(dataset: str, id: int) -> str:
    """
    Creates object store upload path
    """

    return (
        LakePath()
        .dataset(dataset)
        .status(Status.staged)
        .extract_date(pd.today().date())
        .id(id)
        .join(f"{dataset}.parquet")
        .render()
    )
