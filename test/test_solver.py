import pytest

import jsonschema as js
import python_jsonschema_objects as pjs

core_schema = \
{
  "definitions": {
    "name": {
      "type": "string",
    },
    'attr': {'type': 'object', 'properties': {
      'name': {"$ref": "#/definitions/name"},
      'value': {"oneOf": [{ "type": "string" }, { "type": "number" }]},
    }},
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
  'type': 'object', 'title': 'core', 'properties': {
    'transport': {'type': 'object', 'title': 'transport', 'properties': {
      'models': {"type": "array", "items": [{"$ref": "#/definitions/model"}]},
      'categories': {"type": "array", "items": [{"$ref": "#/definitions/category"}]}
    }}
  }
}

def test_core():
    with pytest.raises(js.exceptions.ValidationError):
        instance = {'transport': {
          'models': [{'name': 'a', 'attrs': ['x', 'y']}, {'name': 'b', 'attrs': ['z']}],
          'categories': [{'name': 'viscosity', 'models': ['b']}]
        }}
        js.validate(instance, core_schema)

    instance = {'transport': {
      'models': [{'name': 'a', 'attrs': [{'name': 'x', 'value': 1}, {'name': 'y', 'value': 'abc'}]}]
    }}
    js.validate(instance, core_schema)

    builder = pjs.ObjectBuilder(core_schema)
    ns = builder.build_classes()

    attr = ns.Attr()
    attr.value = 1
    # with pytest.raises(pjs.validators.ValidationError):
    #   attr.value = ''
