# stdlib
from pathlib import Path
import re
import unittest

# pyramid testing requirements
from pyramid import testing
from mako.template import Template
from pyramid.response import Response
from pyramid.request import Request

from pyramid_debugtoolbar_ajax.panels import ajax

# ------------------------------------------------------------------------------


# used to ensure the toolbar link is injected into requests
re_toolbar_link = re.compile(r'(?:href="http://localhost)(/_debug_toolbar/[\d]+)"')


class TestDebugtoolbarPanel(unittest.TestCase):
    def setUp(self):
        self.config = config = testing.setUp()
        config.add_settings({"debugtoolbar.includes": ["pyramid_debugtoolbar_ajax"]})
        config.include("pyramid_debugtoolbar")
        self.settings = config.registry.settings

        # create a view
        def empty_view(request):
            return Response(
                "<html><head></head><body>OK</body></html>", content_type="text/html"
            )

        config.add_view(empty_view)

    def tearDown(self):
        testing.tearDown()

    def test_panel_injected(self):

        # make the app
        app = self.config.make_wsgi_app()
        # make a request
        req1 = Request.blank("/")
        req1.remote_addr = "127.0.0.1"
        resp1 = req1.get_response(app)
        self.assertEqual(resp1.status_code, 200)
        self.assertIn("http://localhost/_debug_toolbar/", resp1.text)

        # check the toolbar
        links = re_toolbar_link.findall(resp1.text)
        self.assertIsNotNone(links)
        self.assertIsInstance(links, list)
        self.assertEqual(len(links), 1)
        toolbar_link = links[0]

        req2 = Request.blank(toolbar_link)
        req2.remote_addr = "127.0.0.1"
        resp2 = req2.get_response(app)
        self.assertEqual(resp2.status_code, 200)

        self.assertIn('<li class="" id="pDebugPanel-Ajax">', resp2.text)
        self.assertIn(
            '<div id="pDebugPanel-Ajax-content" class="panelContent" style="display: none;">',
            resp2.text,
        )
        self.assertIn(
            """<div class="pDebugPanelTitle">
              <h3>Ajax</h3>
            </div>""",
            resp2.text,
        )


class TestAjaxReplay(unittest.TestCase):
    def render_replay(self, request: Request) -> str:
        """Render the panel with the toolbar renderer's default HTML filter."""
        template_path = ajax.AjaxDebugPanel.template.split(":", 1)[1]
        panel_dir = Path(ajax.__file__).parent
        return Template(
            filename=str(panel_dir / template_path), default_filters=["h"]
        ).render(request=request)

    def test_get_replay_preserves_mount_and_query(self) -> None:
        request = Request.blank("/caf%C3%A9?item=one&item=two")
        request.script_name = "/app"
        request.environ.pop("HTTP_HOST", None)
        output = self.render_replay(request)
        self.assertIn('href="/app/caf%C3%A9?item=one&amp;item=two"', output)
        self.assertIn('rel="noopener"', output)

    def test_get_without_query(self) -> None:
        output = self.render_replay(Request.blank("/search"))
        self.assertIn('href="/search"', output)

    def test_replay_requires_local_path(self) -> None:
        request = Request.blank("/")
        request.path_info = "//other.example/path"
        self.assertNotIn('target="_blank"', self.render_replay(request))

    def test_post_replay_preserves_repeated_fields(self) -> None:
        request = Request.blank(
            "/submit?draft=1&mode=edit",
            POST=[("item", 'a"b'), ("item", "c&d"), ("x<y", "")],
        )
        output = self.render_replay(request)
        self.assertIn('action="/submit?draft=1&amp;mode=edit"', output)
        self.assertIn('rel="noopener"', output)
        self.assertEqual(output.count('name="item"'), 2)
        self.assertIn('value="a&#34;b"', output)
        self.assertIn('value="c&amp;d"', output)
        self.assertIn('name="x&lt;y"', output)

    def test_unsupported_post_bodies_have_no_replay_form(self) -> None:
        for content_type in (
            "application/json",
            "multipart/form-data",
            "application/x-www-form-urlencoded; charset=iso-8859-1",
        ):
            with self.subTest(content_type=content_type):
                request = Request.blank(
                    "/submit", method="POST", content_type=content_type, body=b"x=1"
                )
                self.assertNotIn("<form", self.render_replay(request))
