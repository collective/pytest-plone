"""Fixtures used in content tests."""

from plone.dexterity.fti import DexterityFTI
from plone.dexterity.interfaces import IDexterityFTI
from Products.CMFPlone.Portal import PloneSite
from pytest_plone import _types as t
from zope.component import queryUtility

import pytest


@pytest.fixture()
def get_fti(portal: PloneSite) -> t.FTIGetter:
    """Provides a method to get the Factory Type Information for a type by name.

    Example usage:
    ```python
    def test_fti(self, get_fti):
        fti = get_fti("Person")
        assert isinstance(fti, IDexterityFTI)
        assert fti.title == "Person"
    ```
    """

    def get_fti(name: str) -> DexterityFTI:
        """Get the Factory Type Information for a type by name."""
        return queryUtility(IDexterityFTI, name=name)

    return get_fti


@pytest.fixture()
def get_behaviors(get_fti: t.FTIGetter) -> t.BehaviorsGetter:
    """Provides a method to get the list of behaviors for a type.

    Example usage:
    ```python
    def test_behaviors(self, get_behaviors):
        behaviors = get_behaviors("Person")
        assert "plone.namefromtitle" in behaviors
    ```
    """

    def get_behaviors(name: str) -> list[str]:
        """Get the list of behaviors for a content type."""
        fti = get_fti(name)
        return list(fti.behaviors)

    return get_behaviors
