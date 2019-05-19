"""Defines OpenFOAM metamodel common functionality
"""
from typing import Dict, List, Set, Any
import jsonschema as js


JSDocument = Dict[str, Any]  #: typedef on JSON document
JSSchema = Dict[str, Any]  #: typedef on JSON schema

Name = str  #: typedef on entity 'name'
Names = List[Name]  #: typedef on entity 'names'

Entity2Attrs = Dict[Name, Names]  #: typedef on entity to 'attrs' mapping

Type = str  #: typedef on entity schema 'type' description
Value = Any  #: typedef on entity 'value'
Attr = Dict[Type, Dict[Name, Value]]  #: typedef on 'attribute'

Attrs = List[Attr]  #: typedef on list of 'attributes'
Models = Dict[Name, Attrs]  #: typedef on list of 'models'


def validate(document: JSDocument, schema: JSSchema) -> None:
    "Enrich native validation mecahnism to simplify handling 'run-time' schemas"
    entry = {'entry': document}
    js.validate(entry, schema)


def definition2schema(schema: JSSchema, entity: Name) -> None:
    "Compose 'run-time' schema"
    entry = {
        'title': 'entry',
        'type': 'object',
        'properties': {'entry': {'$ref': '#/definitions/{}'.format(entity)}},
        'required': ['entry'],
        'additionalProperties': False,
    }
    schema.update(entry)


def categories(model: JSDocument) -> Entity2Attrs:
    "Extracts 'categories' from the given OpenFOAM 'model' description"
    return dict((item['name'], item['models']) for item in model['categories'])


def models(model: JSDocument) -> Models:
    "Extracts 'models' from the given OpenFOAM 'model' description"
    return dict((item['name'], item['attrs']) for item in model['models'])


def attrs2names(attrs: Attrs) -> JSDocument:
    "Repackge 'model' attibutes to 'name' as keys"
    result = {}
    for attr in attrs:
        for typ, body in attr.items():
            value = body.get('value', None)
            name = body['name']
            result[name] = {'type': typ, 'value': value}

    return result


def validate_transport(document: JSDocument) -> None:
    "Validates the 'transport' model document against 'core' schema"
    category2models = categories(document)
    names: Set[Name] = set()
    for value in category2models.values():
        names.update(value)

    model2attrs = models(document)
    assert set(names) <= set(model2attrs)


def validate_model(document: JSDocument, schema: JSSchema) -> None:
    "Validates the 'core model' document against its schema"
    validate(document, schema)

    validate_transport(document['transport'])


def validate_solver(solver_document: JSDocument, solver_schema: JSSchema, model_document: JSDocument) -> None:
    "Validates the 'solver' document against its schema"
    validate(solver_document, solver_schema)

    category2models = categories(model_document['transport'])
    assert solver_document['transport'] in category2models
