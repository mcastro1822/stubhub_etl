"""
Queries from Stubub 
"""

import httpx
from fake_useragent import UserAgent
from prefect import flow, task

from stubhub.task_handler import TaskManager

client: httpx.AsyncClient = httpx.AsyncClient()


@task(task_run_name="s", retries=3)
async def query_events(stubhub_name: str, stubhub_id: int, pageIndex: int = 0) -> dict:
    """
    Queries event based on PageIndex
    """

    headers = {"User-Agent": UserAgent().random}

    params = {
        "pageIndex": pageIndex,
        "method": "GetFilteredEvents",
        "categoryId": "21651",
        "nearbyGridRadius": "50",
    }

    url: str = f"https://www.stubhub.com/{stubhub_name}/performer/{stubhub_id}"

    r = await client.post(url, headers=headers, params=params, json=params)

    return r.json()


@flow
async def list_events(stubhub_name: str, stubhub_id: int):
    """
    Lists upcoming events
    """

    first_page: dict = await query_events(stubhub_name, stubhub_id)

    max_pages = (first_page["totalCount"] // first_page["pageSize"]) + (
        (first_page["totalCount"] % first_page["pageSize"] != 0) + 1
    )

    async with TaskManager() as tm:
        for page_index in range(1, max_pages):
            await tm.run(query_events, stubhub_name, stubhub_id, page_index)
