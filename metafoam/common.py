"""Defines OpenFOAM metamodel common functionality
"""
from typing import Dict, List, Set
import jsonschema as js

JSDocument = Dict  #: typedef on JSON document
JSSchema = Dict  #: typedef on JSON schema

Name = str  #: typedef on entity 'name'
Names = List[Name]  #: typedef on entity 'names'


def categories(model: JSDocument) -> Dict[Name, Names]:
    "Extracts 'categories' from the given OpenFOAM 'model' description"
    return dict((item['name'], item['models']) for item in model['categories'])


def models(model: JSDocument) -> Dict[Name, Names]:
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
