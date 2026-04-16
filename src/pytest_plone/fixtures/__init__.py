"""Fixtures provided by pytest-plone."""

from .addons import apply_profiles
from .addons import browser_layers
from .addons import controlpanel_actions
from .addons import installer
from .addons import profile_last_version
from .addons import setup_tool
from .addons import uninstalled
from .base import app
from .base import functional_app
from .base import functional_http_request
from .base import functional_portal
from .base import http_request
from .base import portal
from .content import create_content
from .content import get_behaviors
from .content import get_fti
from .env import generate_mo
from .security import grant_roles
from .vocabularies import get_vocabulary

import pytest


__all__ = [
    "app",
    "apply_profiles",
    "browser_layers",
    "controlpanel_actions",
    "create_content",
    "functional_app",
    "functional_http_request",
    "functional_portal",
    "generate_mo",
    "get_behaviors",
    "get_fti",
    "get_vocabulary",
    "grant_roles",
    "http_request",
    "installer",
    "portal",
    "profile_last_version",
    "setup_tool",
    "uninstalled",
]


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "portal(profiles=None, content=None, roles=None): "
        "configure the portal fixture with GenericSetup profiles, "
        "pre-created content, and/or user roles",
    )
