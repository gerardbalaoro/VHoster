"""Services CLI Commands"""
from .core import *


@main.command()
@click.argument('services', nargs=-1, required=False)
@pass_state
def start(state, services):
    """Restart all or specified services"""

    def selected(service):
        return not services or service in services

    if selected('apache'):
        state.server.restart()


@main.command()
@click.argument('services', nargs=-1, required=False)
@pass_state
def stop(state, services):
    """Stop all or specified services"""

    def selected(service):
        return not services or service in services

    if selected('apache'):
        state.server.stop()

    if selected('ngrok'):
        state.ngrok.stop()

    
