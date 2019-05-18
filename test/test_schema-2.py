import pytest

import jsonschema as js
import python_jsonschema_objects as pjs


@pytest.fixture
def core_schema():
    return {
        "definitions": {
            'x-type': {'title': 'XType', 'type': 'object', 'properties': {
                'value': {'type': 'number'},
                'name': {'type': 'string'},
            }, 'required': ['name'], 'additionalProperties': False},
            'x-attr': {'title': 'XAttr', 'type': 'object', 'properties': {
              'x_attr': {'$ref': '#/definitions/x-type'},
            }, 'required': ['x_attr'], 'additionalProperties': False},
            'y-type': {'title': 'YType', 'type': 'object', 'properties': {
                'value': {'type': 'string'},
                'name': {'type': 'string'},
            }, 'required': ['name'], 'additionalProperties': False},
            'y-attr': {'title': 'YAttr', 'type': 'object', 'properties': {
              'y_attr': {'$ref': '#/definitions/y-type'},
            }, 'required': ['y_attr'], 'additionalProperties': False},
            'attrs': {'title': 'TAttr', 'type': 'array', 'items': {'oneOf': [
                {'$ref': '#/definitions/x-attr'},
                {'$ref': '#/definitions/y-attr'},
            ]}, 'additionalItems': False, 'uniqueItems': True},
        },
    }


def validate(document, schema):
    test = {'test': document}
    js.validate(test, schema)


def test_attrs(core_schema):
    test_schema = {
        'title': 'test', 'type': 'object', 'properties': {
            'test': {'$ref': '#/definitions/attrs'},
        },
    }
    core_schema.update(test_schema)

    document = [
        {'x_attr': {'name': 'x', 'value': 1}},
        {'y_attr': {'name': 'y', 'value': '1'}},
    ]
    validate(document, core_schema)

    with pytest.raises(js.exceptions.ValidationError):
        document = [
            {'x_attr': {'name': 'x', 'value': 1}},
            {'x_attr': {'name': 'x', 'value': 1}},
        ]
        validate(document, core_schema)  # check on 'uniqueItems'

    document = [
        {'y_attr': {'name': 'y', 'value': '1'}},
        {'y_attr': {'name': 'y', 'value': '2'}},
    ]
    validate(document, core_schema)  # check on 'uniqueItems'

    with pytest.raises(js.exceptions.ValidationError):
        validate([{'a': 'b'}], core_schema)  # check on 'additionalItems'


def test_x_attr(core_schema):
    test_schema = {
        'title': 'test', 'type': 'object', 'properties': {
            'test': {'$ref': '#/definitions/x-attr'},
        },
    }
    core_schema.update(test_schema)

    validate({'x_attr': {'name': 'x', 'value': 1}}, core_schema)

    validate({'x_attr': {'name': 'x'}}, core_schema)

    with pytest.raises(js.exceptions.ValidationError):
        validate({'x_attr': {'value': 1}}, core_schema)

    with pytest.raises(js.exceptions.ValidationError):
        validate({'x_attr': {}}, core_schema)

    builder = pjs.ObjectBuilder(core_schema)
    ns = builder.build_classes(strict=True, named_only=False, standardize_names=False)

    with pytest.raises(pjs.validators.ValidationError):
        ns.XType()

    x = ns.XType(name='x1')
    assert x.name == 'x1'
    assert x.value is None

    with pytest.raises(pjs.validators.ValidationError):
        x.dummy = 1

    with pytest.raises(pjs.validators.ValidationError):
        x.value = 'txt'

    x.value = 10
    assert x.value == 10
