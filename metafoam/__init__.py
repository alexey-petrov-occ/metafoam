"""Defines metamodel for OpenFOAM
"""

from typing import Dict

JSDocument = Dict

def categories(model: JSDocument) -> Dict:
    "Extracts 'categories' from the given OpenFOAM 'model' description"
    return dict((item['name'], item['models']) for item in model['categories'])

def models(model: JSDocument) -> Dict:
    "Extracts 'models' from the given OpenFOAM 'model' description"
    return dict((item['name'], item['attrs']) for item in model['models'])
