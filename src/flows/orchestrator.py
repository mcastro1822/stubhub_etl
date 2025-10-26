from prefect import flow

from stubhub.blocks import blocks
from stubhub.models import StubhubRepo


@flow
async def orchestrator():
    """
    Manages excution of stubhub scrape
    """

    StubhubRepo((blocks.mongodb).get_client()["production"])
