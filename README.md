pyramid_debugtoolbar_ajax
=========================

This package adds an "Ajax" panel to the `pyramid_debugtoolbar`.

The "Ajax" panel contains buttons and forms which can be used to replay the
request in a new browser window -- allowing you to spawn a debugger window for
errors encountered on background ajax requests, or form submissions.

How to use:

Add this to your pyramid includes:

    pyramid.includes = pyramid_debugtoolbar
    debugtoolbar.includes = pyramid_debugtoolbar_ajax
