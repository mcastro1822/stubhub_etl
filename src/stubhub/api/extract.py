"""
Queries from Stubub 
"""

import httpx
from fake_useragent import UserAgent
from prefect import task

client: httpx.AsyncClient = httpx.AsyncClient()


@task(task_run_name="Query Index {pageIndex}", retries=3)
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
