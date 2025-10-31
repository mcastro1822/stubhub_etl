"""
Context Manager for Async Task Result Retrieval
"""

from functools import partial
from typing import Callable

import anyio
from anyio.abc import TaskGroup


class TaskManager:
    """
    Manages Task Async Execution
    """

    def __init__(self, concurrency: int = 6):
        self.task_group: TaskGroup = anyio.create_task_group()
        self.results: list | None = None
        self.semaphore = anyio.Semaphore(concurrency)

    async def __aenter__(self):
        """
        Enters Context Manager
        """
        await self.task_group.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ):
        """
        Exits Context Manager
        """
        await self.task_group.__aexit__(exc_type, exc_val, exc_tb)

    async def __run(self, func: Callable, *args):
        """
        Runs with semaphore
        """
        async with self.semaphore:
            r = await func(*args)

            self.results.append(r)

    async def run(self, func: Callable, *args, **kwargs):
        """
        Creates nursery for task execution
        """
        self.results = []

        partial_func = partial(func, **kwargs)

        self.task_group.start_soon(self.__run, partial_func, *args)
