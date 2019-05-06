import pytest
import jsonschema as js

models_schema = \
{
  "definitions": {
    'attr': {
      "type": "string",
    },
    "attrs": {
      "type": "array",
      "items": [
        {
          "$ref": "#/definitions/attr"
        }
      ]
    },
    'model': {
      'type': 'object', 'properties': {
        'name': {'type': 'string'},
        'attrs': {'$ref': '#/definitions/attrs'},
      }
    },
    "name": {
      "type": "string",
    },
    "names": {
      "type": "array",
      "items": [
        {
          "$ref": "#/definitions/name"
        }
      ]
    },
    'category': {
      'type': 'object', 'properties': {
        'name': {'type': 'string'},
        'models': {"$ref": "#/definitions/names"}
      }
    }
  },
  'title': 'core',
  'type': 'object', 'properties': {
    'transport': {'type': 'object', 'properties': {
      'models': {"type": "array", "items": [{"$ref": "#/definitions/model"}]},
      'categories': {"type": "array", "items": [{"$ref": "#/definitions/category"}]}
    }}
  },
  "required": ["transport"], 
  "minProperties": 1, "maxProperties": 1,
}

def test_translation():
    with pytest.raises(js.exceptions.ValidationError):
        source = {'a': ['x', 'y'], 'b': ['z'], 'c': []}
        js.validate(source, models_schema)

    with pytest.raises(js.exceptions.ValidationError):
        source = {'transport': {}, 'x': {}}
        js.validate(source, models_schema)
    target = {'transport': {
      'models': [{'name': 'a', 'attrs': ['x', 'y']},
       {'name': 'b', 'attrs': ['z']}],
      'categories': [{'name': 'viscosity', 'models': ['b']}]
    }}
    
    js.validate(target, models_schema)