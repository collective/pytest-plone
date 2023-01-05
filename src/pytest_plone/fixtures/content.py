"""Fixtures used in content tests."""
from plone.dexterity.fti import DexterityFTI
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import queryUtility

import pytest


@pytest.fixture()
def get_fti():
    def get_fti(name: str) -> DexterityFTI:
        """Get the fti for a type by name."""
        return queryUtility(IDexterityFTI, name=name)

    return get_fti


@pytest.fixture()
def get_behaviors(get_fti):
    def get_behaviors(name: str) -> list:
        """Get the list of behaviors for a content type."""
        fti = get_fti(name)
        return list(fti.behaviors)

    return get_behaviors
