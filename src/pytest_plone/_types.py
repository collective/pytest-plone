from OFS.SimpleItem import Item
from plone.app.vocabularies import PermissiveVocabulary
from plone.app.vocabularies import SlicableVocabulary
from plone.dexterity.content import DexterityContent
from plone.dexterity.fti import DexterityFTI
from typing import Protocol
from typing import TypeAlias
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import TreeVocabulary


Context: TypeAlias = DexterityContent | Item

PloneVocabulary: TypeAlias = (
    SimpleVocabulary | TreeVocabulary | PermissiveVocabulary | SlicableVocabulary
)


class ProfileVersionGetter(Protocol):
    def __call__(self, profile: str) -> str: ...


class FTIGetter(Protocol):
    def __call__(self, name: str) -> DexterityFTI: ...


class BehaviorsGetter(Protocol):
    def __call__(self, name: str) -> list[str]: ...


class VocabularyGetter(Protocol):
    def __call__(self, name: str, context: Context) -> PloneVocabulary: ...
