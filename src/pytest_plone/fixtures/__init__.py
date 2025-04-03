"""Fixtures provided by pytest-plone."""

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
from .env import generate_mo
from .playwright import playwright_page_factory
from .playwright import portal_factory
from .vocabularies import get_vocabulary


__all__ = [
    "app",
    "browser_layers",
    "controlpanel_actions",
    "generate_mo",
    "get_behaviors",
    "get_fti",
    "get_vocabulary",
    "http_request",
    "installer",
    "playwright_page_factory",
    "portal",
    "portal_factory",
    "profile_last_version",
    "setup_tool",
]
