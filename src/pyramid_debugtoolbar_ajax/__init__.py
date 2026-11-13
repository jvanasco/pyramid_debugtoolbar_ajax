from pyramid.config import Configurator

from .panels.ajax import AjaxDebugPanel

__VERSION__ = "1.0.0"


def includeme(config: Configurator) -> None:
    """Register the Ajax panel with the debug toolbar."""
    config.add_debugtoolbar_panel(AjaxDebugPanel)
