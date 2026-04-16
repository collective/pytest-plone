"""Marker support for pytest-plone fixtures."""

from plone import api
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.PortalContent import PortalContent
from Products.CMFPlone.Portal import PloneSite
from zope.component.hooks import site

import pytest


PORTAL_MARKER_NAME: str = "portal"


def apply_profiles(portal: PloneSite, profiles: list[str]) -> None:
    """Apply GenericSetup profiles to a Plone site.

    Each entry can be either ``"my.addon:default"`` or the full
    ``"profile-my.addon:default"`` form — the ``profile-`` prefix
    is added automatically when missing.
    """
    with site(portal):
        setup_tool = api.portal.get_tool("portal_setup")
        for profile_id in profiles:
            if not profile_id.startswith("profile-"):
                profile_id = f"profile-{profile_id}"
            setup_tool.runAllImportStepsFromProfile(profile_id)


def create_content(container: PortalContent, content: list[dict]) -> None:
    """Create content items in a container.

    Each dict in *content* is passed as keyword arguments to
    ``plone.api.content.create(container=container, **spec)``.
    """
    for spec in content:
        api.content.create(container=container, **spec)


def grant_roles(context: PortalContent, roles: list[str]) -> None:
    """Grant roles to the default test user."""
    api.user.grant_roles(username=TEST_USER_ID, roles=roles, obj=context)


def apply_portal_marker(portal: PloneSite, request: pytest.FixtureRequest) -> None:
    """Read ``@pytest.mark.portal`` and apply profiles, content, and roles."""
    marker = request.node.get_closest_marker(PORTAL_MARKER_NAME)
    if marker is None:
        return
    marker_profiles: list[str] = marker.kwargs.get("profiles", [])
    marker_content: list[dict] = marker.kwargs.get("content", [])
    marker_roles: list[str] = marker.kwargs.get("roles", [])
    with site(portal):
        if marker_profiles:
            apply_profiles(portal, marker_profiles)
        if marker_content:
            with api.env.adopt_user(SITE_OWNER_NAME):
                create_content(portal, marker_content)
        if marker_roles:
            grant_roles(portal, marker_roles)
