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

solver_schema = \
{
  "definitions": {
    'x-attr': {'title': 'XAttr', 'type': 'object', 'properties': {
      'value': {'type': 'number'}
    }, 'additionalProperties': False},
    'x': {'type': 'object', 'properties': {
      'x' : {'$ref': '#/definitions/x-attr'},
    }, 'additionalProperties': False},
    'y-attr': {'title': 'YAttr', 'type': 'object', 'properties': {
      'name': {'type': 'string'},
      'value': {'type': 'string'},
    }, "required": ["name"], 'additionalProperties': False},
    'y': {'type': 'object', 'properties': {
      'y_attr' : {'$ref': '#/definitions/y-attr'},
    }, 'additionalProperties': False},
    'z-attr': {'title': 'ZAttr', 'type': 'object', 'properties': {
      'z': {'type': 'string'}
    }, 'additionalProperties': False},
    'z': {'type': 'object', 'properties': {
      'z-type' : {'$ref': '#/definitions/z-attr'},
    }, 'additionalProperties': False},
     'Attrs': {'type': 'array', 'items': {'oneOf': [
      {'$ref': '#/definitions/x'},
      {'$ref': '#/definitions/y'},
    ]}, "additionalItems": False},
  },
  'title': 'Test', 'type': 'object', 'properties': {
    'x': {'$ref': '#/definitions/x-attr'},
    'y-attr': {'$ref': '#/definitions/y-attr'},
    'attrs': {'$ref': '#/definitions/Attrs'},
    'simple-x': {'$ref': '#/definitions/x'},
    'array-x': {'type': 'array', 'items': [
      {'$ref': '#/definitions/x'},
    ]},
    'simple-z': {'$ref': '#/definitions/z'},
    'array-xz': {'type': 'array', 'items': {'oneOf': [
      {'$ref': '#/definitions/x'},
      {'$ref': '#/definitions/z'},
     ]}},
  }
}

def test_attrs():
    js.validate({'simple-x': {'x': {'value': 1}}}, solver_schema)

    js.validate({'array-x': [{'x': {'value': 1}}]}, solver_schema)

    js.validate({'array-xz': [{'x': {'value': 1}}]}, solver_schema)

    js.validate({'simple-z': {'z-type': {'z': 'abc'}}}, solver_schema)

    instance = {'array-xz': [{'x': {'value': 1}},
                             {'z-type': {'z': 'abc'}}]}
    js.validate(instance, solver_schema)

    instance = {'attrs': [{'x': {'value': 1}},
                          {'y_attr': {'name': 'a', 'value': 'abc'}}]}
    js.validate(instance, solver_schema)

    with pytest.raises(js.exceptions.ValidationError):
        instance = {'attrs': [{'y_attr': {'name': 'y', 'value': 1}}]}
        js.validate(instance, solver_schema)

    builder = pjs.ObjectBuilder(solver_schema)
    ns = builder.build_classes(strict=True, named_only=False, standardize_names=False)

    x = ns.XAttr()
    attrs = ns.Attrs([x])
    assert attrs.validate()
    assert len(attrs) == 1

    y_attr = ns.YAttr(name='y') # create a specific schema instance
    assert y_attr.value is None # check its not initialized attribute values
    assert y_attr.validate()

    y_attr.value = 'a' # check that proper type values are accepted
    with pytest.raises(pjs.validators.ValidationError):
        y_attr.dummy = 'a' # expected fail on non specified attibute usage
    with pytest.raises(pjs.validators.ValidationError):
        y_attr.value = 1 # expected fail on non proper type value assignment
    assert y_attr.value == 'a' # check that previously stored value stays unchanged

    attrs.insert(0, y_attr) # check that any object can be put into collection
    assert len(attrs) == 2
    with pytest.raises(pjs.validators.ValidationError):
        attrs.validate() # collection can be validated later on

    del attrs[y_attr] # object can be deleted from the collection
    assert len(attrs) == 1

    y = ns.y()
    attrs.append(ns.y())
    assert attrs.validate()
    assert len(attrs) == 2

    attrs.append(1)
    with pytest.raises(pjs.validators.ValidationError):
        attrs.validate()

    with pytest.raises(js.exceptions.ValidationError):
        js.validate({'attrs': [1]}, solver_schema)


def test_xattr():
    js.validate({'x': {'value': 1}}, solver_schema)

    with pytest.raises(js.exceptions.ValidationError):
        js.validate({'x': {'value': ''}}, solver_schema)

    builder = pjs.ObjectBuilder(solver_schema)
    ns = builder.build_classes(named_only=True, standardize_names=False)
    x = ns.XAttr()

    x.value = 1
    assert x.value == 1

    with pytest.raises(pjs.validators.ValidationError):
      x.value = ''
    assert x.value == 1

def test_yattr():
    js.validate({'y-attr': {'name': 'y', 'value': ''}}, solver_schema)

    with pytest.raises(js.exceptions.ValidationError):
        js.validate({'y-attr': {'name': 'y', 'value': 1}}, solver_schema)

    builder = pjs.ObjectBuilder(solver_schema)
    ns = builder.build_classes(named_only=True, standardize_names=False)
    y = ns.YAttr()

    y.value = ''
    assert y.value == ''

    with pytest.raises(pjs.validators.ValidationError):
        y.value = 1
    assert y.value == ''

    with pytest.raises(pjs.validators.ValidationError):
        y.validate()

    y.name = 'y'
    assert y.validate()
