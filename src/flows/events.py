"""
Collects events table

"""

import anyio
import polars as pl
from prefect import flow

from stubhub.api.extract import query_events
from stubhub.api.task_handler import TaskManager
from stubhub.blocks import blocks
from stubhub.mongodb.models import Query, StubhubRepo
from stubhub.object_store.load import load_to_object_store
from stubhub.object_store.pathing import staging_path
from stubhub.transform.stage import json_to_df


@flow(name="List Events - {stubhub_name}", description="Lists Future Events")
async def list_events(stubhub_name: str, stubhub_id: int):
    """
    Lists upcoming events by name and id

    Args:
        stubhub_name (str): stubhub artist / event name
        stubhub_id (int): stubhub artist / event id

    """

    first_page: dict = await query_events(stubhub_name, stubhub_id)

    max_pages = (first_page["totalCount"] // first_page["pageSize"]) + (
        (first_page["totalCount"] % first_page["pageSize"] != 0) + 1
    )

    async with TaskManager() as tm:
        for page_index in range(1, max_pages):
            await tm.run(query_events, stubhub_name, stubhub_id, page_index)

    df: pl.DataFrame = json_to_df(tm.results, stubhub_name, stubhub_id)

    landing_path: str = staging_path("listings", stubhub_id)

    await load_to_object_store(df, landing_path)


@flow(name="Events Orchestrator")
async def events_orchestrator():
    """
    Manages excution of stubhub events
    """

    repo: StubhubRepo = StubhubRepo((blocks.mongodb).get_client()["production"])

    event_configs: list[Query] = repo.get_all()

    async with anyio.create_task_group() as tg:

        for event_config in event_configs:
            tg.start_soon(
                list_events, event_config.stubhub_name, event_config.stubhub_id
            )
