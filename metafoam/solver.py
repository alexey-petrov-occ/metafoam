"""Defines Solver metamodel for OpenFOAM
"""
from .common import JSDocument, JSSchema, Name, Names
from .common import categories, models, validate_solver


class Solver:
    "Provides semantic level validation and programming API for an OpenFOAM solver"
    __slots__ = ('_solver', '_model', '_transport_model')

    def __init__(self, solver_document: JSDocument, solver_schema: JSSchema, model_document: JSDocument):
        validate_solver(solver_document, solver_schema, model_document)
        self._solver = solver_document
        self._model = model_document
        self._transport_model: Name = ''

    @property
    def transport(self) -> Name:
        "Retruns conamed property"
        return self._solver['transport']

    @transport.setter
    def transport(self, value: Name) -> None:
        "Updates conamed property"
        category2models = categories(self._model['transport'])
        assert value in category2models

        self._solver['transport'] = value
        self._transport_model = ''

    @property
    def transport_model(self) -> Name:
        "Retruns conamed property"
        return self._transport_model

    @transport_model.setter
    def transport_model(self, value: Name) -> None:
        "Updates conamed property"
        category2models = categories(self._model['transport'])
        assert value in category2models[self.transport]

        self._transport_model = value

    @property
    def transport_attrs(self) -> Names:
        "Retruns conamed property"
        assert self._transport_model != ''

        model2attrs = models(self._model['transport'])
        return model2attrs[self._transport_model]
