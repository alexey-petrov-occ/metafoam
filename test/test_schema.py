import pytest

import jsonschema
from jsonschema import validate

def test_basic():
    # A sample schema, like what we'd get from json.load()
    schema = {
        "type" : "object",
        "properties" : {
            "price" : {"type" : "number"},
            "name" : {"type" : "string"},
        },
    }

    # If no exception is raised by validate(), the instance is valid.
    validate(instance={"name" : "Eggs", "price" : 34.99}, schema=schema)

    with pytest.raises(jsonschema.exceptions.ValidationError):
        validate(
            instance={"name" : "Eggs", "price" : "Invalid"}, schema=schema,
        )

array_schema = \
{
  "$id": "https://example.com/geographical-location.schema.json",
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Longitude and Latitude Values",
  "description": "A geographical coordinate.",
  "type": "array",
  "items": [
    {
      "type": "string"
    }
  ]
}

def test_array():
    text = """
k
n
nu0
nuInf
"""
    instance = text.splitlines()
    validate(instance, array_schema)

attrs_schema = \
{
  'defs': {
    'attr': {
      "type": "string",
    },
    "attrs": {
      "type": "array",
      "items": [
        {
          "$ref": "#/defs/attr"
        }
      ]
    },
  },
  'type': 'object', 'properties': {
    'attrs': {"$ref": "#/defs/attrs"}
  }
}

def test_attrs():
    instance = {'attrs': ['x', 'y']}
    validate(instance, attrs_schema)

model_schema = \
{
  'defs': {
    'attr': {
      "type": "string",
    },
    "attrs": {
      "type": "array",
      "items": [
        {
          "$ref": "#/defs/attr"
        }
      ]
    },
    'model': {
      'type': 'object', 'properties': {
        'name': {'type': 'string'},
        '$ref': '#/defs/attrs'
      }
    }
  },
  "type": "array", "items": [{"$ref": "#/defs/model"}]
}

def test_model():
    instance = [{'name': 'a', 'attrs': ['x', 'y']}, {'name': 'b', 'attrs': ['z']}]
    validate(instance, model_schema)

models_schema = \
{
  "defs": {
    'attr': {
      "type": "string",
    },
    "attrs": {
      "type": "array",
      "items": [
        {
          "$ref": "#/defs/attr"
        }
      ]
    },
    'model': {
      'type': 'object', 'properties': {
        'name': {'type': 'string'},
        '$ref': '#/defs/attrs'
      }
    },
    "name": {
      "type": "string",
    },
    "names": {
      "type": "array",
      "items": [
        {
          "$ref": "#/defs/name"
        }
      ]
    },
    'category': {
      'type': 'object', 'properties': {
        'name': {'type': 'string'},
        'models': {"$ref": "#/defs/names"}
      }
    }
  },
  'type': 'object', 'properties': {
    'transport': {'type': 'object', 'properties': {
      'models': {"type": "array", "items": [{"$ref": "#/defs/model"}]},
      'categories': {"type": "array", "items": [{"$ref": "#/defs/category"}]}
    }}
  }
}

def test_models():
    instance = {'transport': {
      'models': [{'name': 'a', 'attrs': ['x', 'y']}, {'name': 'b', 'attrs': ['z']}],
      'categories': [{'name': 'viscosity', 'models': ['b']}]
    }}
    validate(instance, models_schema)

solver_schema = \
{
  'title': 'solver',
  'defs': {
    'category': {"type": "string"},
  },
 'type': 'object', 'properties': {
    'transport': {"$ref": "#/defs/category"},
  },
}

def test_solver():
    instance = {'transport': 'viscosity'}
    validate(instance, solver_schema)

from typing import Dict, Set

JSDocument = Dict
JSSchema = Dict
Name = str

def categories(model: JSDocument) -> Dict:
    return dict((item['name'], item['models']) for item in model['categories'])

def validate_model(document: JSDocument, schema: JSSchema) -> None:
    validate(document, schema)
    category2models = categories(document['transport'])
    models: Set[Name] = set()
    for value in category2models.values():
        models.update(value)

    model2attrs = dict((item['name'], item['attrs']) for item in document['transport']['models'])
    assert set(models) <= set(model2attrs)

def test_validate_model():
    model = {'transport': {
      'models': [{'name': 'a', 'attrs': ['x', 'y']}, {'name': 'b', 'attrs': ['z']}],
      'categories': [{'name': 'K', 'models': ['b']}, {'name': 'L', 'models': ['a', 'c']}]
    }}
    validate(model, models_schema)

    category2models = categories(model['transport'])
    assert 'K' in category2models
    assert 'a' in category2models['L']

    with pytest.raises(AssertionError):
      validate_model(model, models_schema)

def validate_solver(solver_document: JSDocument, solver_schema: JSSchema, model_document: JSDocument) -> None:
    validate(solver_document, solver_schema)

    category2models = categories(model_document['transport'])
    assert solver_document['transport'] in category2models

def test_validate_solver():
    model = {'transport': {
      'models': [{'name': 'a', 'attrs': ['x', 'y']}, {'name': 'b', 'attrs': ['z']}],
      'categories': [{'name': 'K', 'models': ['b']}, {'name': 'L', 'models': ['a', 'c']}]
    }}

    solver = {'transport': 'K'}
    validate_solver(solver, solver_schema, model)

    with pytest.raises(AssertionError):
      solver = {'transport': 'M'}
      validate_solver(solver, solver_schema, model)

class Solver(object):
    __slots__ = ('_solver', '_model', '_transport_model')
    def __init__(self, solver_document: JSDocument, solver_schema: JSSchema, model_document: JSDocument):
        validate_solver(solver_document, solver_schema, model_document)
        self._solver = solver_document
        self._model = model_document
        self._transport_model: Name = ''

    @property
    def transport(self) -> Name:
        return self._solver['transport']

    @property
    def transport_model(self) -> Name:
        return self._transport_model

    @transport_model.setter
    def transport_model(self, value: Name) -> None:
        category2models = categories(self._model['transport'])
        assert value in category2models[self.transport]

        self._transport_model = value

def validate_slots(instance):
    with pytest.raises(AttributeError):
      setattr(instance, 'dummy', 1)

    return instance

def test_solver_introspection():
    model = {'transport': {
      'models': [{'name': 'a', 'attrs': ['x', 'y']}, {'name': 'b', 'attrs': ['z']}],
      'categories': [{'name': 'K', 'models': ['b']}, {'name': 'L', 'models': ['a', 'c']}]
    }}

    solver = {'transport': 'K'}

    inst = validate_slots(Solver(solver, solver_schema, model))
    assert inst.transport == 'K'

    assert inst.transport_model == ''

    inst.transport_model = 'b'
    assert inst.transport_model == 'b'

    with pytest.raises(AssertionError):
        inst.transport_model = 'a'
