"""All Fixtures."""
from .addons import browser_layers
from .addons import controlpanel_actions
from .addons import installer
from .addons import profile_last_version
from .addons import setup_tool
from .base import app
from .base import http_request
from .base import portal
from .content import get_behaviors
from .content import get_fti
from .vocabularies import get_vocabulary


__all__ = [
    app,
    browser_layers,
    controlpanel_actions,
    get_behaviors,
    get_fti,
    get_vocabulary,
    http_request,
    installer,
    profile_last_version,
    portal,
    setup_tool,
]
