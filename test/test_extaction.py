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
        main={'strainRateFunction': [''], 'Casson': ['m', 'tau0', 'nuMin_', 'nuMax_'], 'CrossPowerLaw': ['nu0', 'nuInf', 'm', 'n'], 'Newtonian': ['nu'], 'powerLaw': ['k', 'n', 'nuMin', 'nuMax'], 'BirdCarreau': ['nu0', 'nuInf', 'k', 'n'], 'HerschelBulkley': ['k', 'n', 'tau0', 'nu0']}
        js.validate(main, models_schema)




    with pytest.raises(js.exceptions.ValidationError):
        source = {'a': ['x', 'y'], 'b': ['z'], 'c': []}
        js.validate(source, models_schema)

    with pytest.raises(js.exceptions.ValidationError):
        source = {'transport': {}, 'x': {}}
        js.validate(source, models_schema)
    target = {'transport': {'models': [{'name': 'strainRateFunction', 'attrs': []}, {'name': 'Casson', 'attrs': ['m', 'tau0', 'nuMin_', 'nuMax_']}, {'name': 'CrossPowerLaw', 'attrs': ['nu0', 'nuInf', 'm', 'n']}, {'name': 'Newtonian', 'attrs': ['nu']}, {'name': 'powerLaw', 'attrs': ['k', 'n', 'nuMin', 'nuMax']}, {'name': 'BirdCarreau', 'attrs': ['nu0', 'nuInf', 'k', 'n']}, {'name': 'HerschelBulkley', 'attrs': ['k', 'n', 'tau0', 'nu0']}], 'categories': [{'name': 'viscosity', 'models': ['strainRateFunction', 'Casson', 'CrossPowerLaw', 'Newtonian', 'powerLaw', 'BirdCarreau', 'HerschelBulkley']}]}}
    
    js.validate(target, models_schema)