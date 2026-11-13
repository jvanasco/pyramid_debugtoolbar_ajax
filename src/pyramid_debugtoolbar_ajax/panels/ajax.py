from typing import Dict

from pyramid.request import Request
from pyramid_debugtoolbar.panels import DebugPanel


class AjaxDebugPanel(DebugPanel):
    """Display the AJAX controls in the debug toolbar."""

    name = "Ajax"
    has_content = True
    template = "pyramid_debugtoolbar_ajax.panels:templates/ajax.dbtmako"

    def __init__(self, request: Request) -> None:
        """Store the request inspected by the toolbar."""
        self.data: Dict[str, Request] = {"request": request}

    @property
    def nav_title(self) -> str:
        """Return the panel label in the toolbar navigation."""
        return self.name

    @property
    def title(self) -> str:
        """Return the heading shown inside the panel."""
        return self.name

    @property
    def url(self) -> str:
        """Return the empty URL for an inline panel."""
        return ""

    def render_content(self, request: Request) -> str:
        """Render the panel using the current toolbar request."""
        self.data["toolbar_request"] = request
        return DebugPanel.render_content(self, request)
