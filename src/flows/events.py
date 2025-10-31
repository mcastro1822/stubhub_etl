"""
Collects events table

"""

import anyio
from prefect import flow

from stubhub.api.extract import list_events
from stubhub.blocks import blocks
from stubhub.mongodb.models import Query, StubhubRepo


@flow
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
