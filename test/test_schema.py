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

def test_show_categories():
    model = {'transport': {
      'models': [{'name': 'a', 'attrs': ['x', 'y']}, {'name': 'b', 'attrs': ['z']}],
      'categories': [{'name': 'K', 'models': ['b']}, {'name': 'L', 'models': ['a', 'c']}]
    }}
    validate(model, models_schema)

    categories = dict((item['name'], item['models']) for item in model['transport']['categories'])
    assert 'K' in categories
    assert 'a' in categories['L']
