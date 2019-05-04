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
    "Validates the 'core model' document against schema"
    js.validate(document, schema)
    category2models = categories(document['transport'])
    names: Set[Name] = set()
    for value in category2models.values():
        names.update(value)

    model2attrs = models(document['transport'])
    assert set(names) <= set(model2attrs)
