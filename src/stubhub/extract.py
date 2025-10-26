"""
Queries from Stubub 
"""

import httpx
from fake_useragent import UserAgent

client: httpx.AsyncClient = httpx.AsyncClient()


async def list_events(stubhub_name: str, stubhub_id: int):
    """
    Lists upcoming events
    """
    headers = {"User-Agent": UserAgent().random}

    params = {}

    url: str = f"https://www.stubhub.com/{stubhub_name}/performer/{stubhub_id}"

    r = await client.post(url, headers=headers, params=params, json=params)

    print(r.json())
