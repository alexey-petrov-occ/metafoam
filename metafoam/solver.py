"""Defines Solver metamodel for OpenFOAM
"""
from .common import JSDocument, JSSchema, Name, Names
from .common import validate_solver, attrs2names

from .core import Core


class Transport:
    "Provides entry point for 'transport' model management"
    __slots__ = ('_document', '_model', '_core')

    def __init__(self, document: JSDocument, core: Core):
        self._document = document
        self._model: Name = ''
        self._core = core

    @property
    def category(self) -> Name:
        "Retruns conamed property"
        return str(self._document['transport'])

    @category.setter
    def category(self, value: Name) -> None:
        "Updates conamed property"
        category2models = self._core.categories('transport')
        assert value in category2models

        self._document['transport'] = value
        self._model = ''

    @property
    def model(self) -> Name:
        "Retruns conamed property"
        return self._model

    @model.setter
    def model(self, value: Name) -> None:
        "Updates conamed property"
        category2models = self._core.categories('transport')
        assert value in category2models[self.category]

        self._model = value

    @property
    def attrs(self) -> Names:
        "Retruns conamed property"
        assert self._model != ''

        model2attrs = self._core.models('transport')
        attrs = model2attrs[self._model]
        names = attrs2names(attrs).keys()
        return list(names)


class Solver:  # pylint: disable=too-few-public-methods
    "Provides semantic level validation and programming API for an OpenFOAM solver"
    __slots__ = ('_document', '_core', '_transport_model', '_transport')

    def __init__(self, document: JSDocument, schema: JSSchema, core: Core):
        validate_solver(document, schema, core.document)
        self._transport_model: Name = ''
        self._document = document
        self._core = core
        self._transport = Transport(document, core)

    @property
    def transport(self) -> Transport:
        "Retruns conamed property"
        return self._transport
