"""
The projects CLI entrypoint
"""

import anyio
import click

from flows.events import events_orchestrator


@click.group()
def cli():
    """
    entrypoint for command group
    """
    ...


@cli.command
def trigger_orch():
    """
    Runs Event Listings Orchestrator
    """
    anyio.run(events_orchestrator)
