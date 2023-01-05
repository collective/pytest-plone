"""Fixtures used to test vocabularies."""
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

import pytest


@pytest.fixture(scope="session")
def get_vocabulary():
    def get_vocabulary(name: str, context) -> SimpleVocabulary:
        """Get a vocabulary by name."""
        return getUtility(IVocabularyFactory, name)(context)

    return get_vocabulary
