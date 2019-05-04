"""Defines metamodel for OpenFOAM
"""
from typing import Dict, Set, List
import jsonschema as js

JSDocument = Dict
JSSchema = Dict

Name = str
Names = List[Name]


def categories(model: JSDocument) -> Dict:
    "Extracts 'categories' from the given OpenFOAM 'model' description"
    return dict((item['name'], item['models']) for item in model['categories'])


def models(model: JSDocument) -> Dict:
    "Extracts 'models' from the given OpenFOAM 'model' description"
    return dict((item['name'], item['attrs']) for item in model['models'])


def validate_model(document: JSDocument, schema: JSSchema) -> None:
    "Validates the 'core model' document against its schema"
    js.validate(document, schema)
    category2models = categories(document['transport'])
    names: Set[Name] = set()
    for value in category2models.values():
        names.update(value)

    model2attrs = models(document['transport'])
    assert set(names) <= set(model2attrs)


def validate_solver(solver_document: JSDocument, solver_schema: JSSchema, model_document: JSDocument) -> None:
    "Validates the 'solver' document against its schema"
    js.validate(solver_document, solver_schema)

    category2models = categories(model_document['transport'])
    assert solver_document['transport'] in category2models


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
