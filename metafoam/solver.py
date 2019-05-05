"""Defines Solver metamodel for OpenFOAM
"""
from .common import JSDocument, JSSchema, Name, Names
from .common import validate_solver

from .core import Core


class Solver:
    "Provides semantic level validation and programming API for an OpenFOAM solver"
    __slots__ = ('_document', '_core', '_transport_model')

    def __init__(self, document: JSDocument, schema: JSSchema, core: Core):
        validate_solver(document, schema, core.document)
        self._transport_model: Name = ''
        self._document = document
        self._core = core

    @property
    def transport(self) -> Name:
        "Retruns conamed property"
        return self._document['transport']

    @transport.setter
    def transport(self, value: Name) -> None:
        "Updates conamed property"
        category2models = self._core.categories('transport')
        assert value in category2models

        self._document['transport'] = value
        self._transport_model = ''

    @property
    def transport_model(self) -> Name:
        "Retruns conamed property"
        return self._transport_model

    @transport_model.setter
    def transport_model(self, value: Name) -> None:
        "Updates conamed property"
        category2models = self._core.categories('transport')
        assert value in category2models[self.transport]

        self._transport_model = value

    @property
    def transport_attrs(self) -> Names:
        "Retruns conamed property"
        assert self._transport_model != ''

        model2attrs = self._core.models('transport')
        return model2attrs[self._transport_model]
