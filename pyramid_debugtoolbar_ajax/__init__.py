from .panels.ajax import AjaxDebugPanel


__VERSION__ = "0.1.4dev0"


def includeme(config):
    config.add_debugtoolbar_panel(AjaxDebugPanel)
