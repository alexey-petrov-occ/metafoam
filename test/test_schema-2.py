import pytest

import jsonschema as js
import python_jsonschema_objects as pjs

from metafoam import common


@pytest.fixture
def solver_schema():
    return {
        'definitions': {
            'category': {'type': 'string'},
            'transport': {'$ref': '#/definitions/category'},
            'solver': {'type': 'object', 'properties': {
                'transport': {'$ref': '#/definitions/transport'},
            }, 'additionalProperties': False},
        },
    }

@pytest.fixture
def core_schema():
    return {
        'definitions': {
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
            'attrs': {'title': 'TAttrs', 'type': 'array', 'items': {'oneOf': [
                {'$ref': '#/definitions/x-attr'},
                {'$ref': '#/definitions/y-attr'},
            ]}, 'additionalItems': False, 'uniqueItems': True},
            'model': {'type': 'object', 'properties': {
                'name': {'type': 'string'},
                'attrs': {'$ref': '#/definitions/attrs'},
            }, 'required': ['name'], 'additionalProperties': False},
            'models': {'type': 'array', 'items': [
                {'$ref': '#/definitions/model'},
            ], 'additionalItems': False, 'uniqueItems': True},
            'names': {'type': 'array', 'items': [
                {'type': 'string'},
            ], 'additionalItems': {'type': 'string'}, 'uniqueItems': True},
            'category': {'type': 'object', 'properties': {
                'name': {'type': 'string'},
                'models': {'$ref': '#/definitions/names'}
            }, 'required': ['name', 'models'], 'additionalProperties': False},
            'categories': {'type': 'array', 'items': {'oneOf': [
                {'$ref': '#/definitions/category'}
            ]}, 'additionalItems': False, 'uniqueItems': True},
            'transport': {'type': 'object', 'properties': {
                'models': {'$ref': '#/definitions/models'},
                'categories': {'$ref': '#/definitions/categories'},
            }, 'required': ['models']},
         },
    }


def validate(document, schema):
    test = {'test': document}
    js.validate(test, schema)


def update_schema(schema, entity):
    test_schema = {
        'title': 'test', 'type': 'object', 'properties': {
            'test': {'$ref': '#/definitions/{}'.format(entity)},
        },
    }
    schema.update(test_schema)
    return schema

def test_solver(solver_schema):
    update_schema(solver_schema, 'solver')

    validate({}, solver_schema)

    validate({'transport': 'A'}, solver_schema)

    with pytest.raises(js.exceptions.ValidationError):
        validate({'a': 'b'}, solver_schema)  # check on 'additionalProperties'


def test_transport(core_schema):
    update_schema(core_schema, 'transport')

    validate({'models': [], 'categories': []}, core_schema)

    with pytest.raises(js.exceptions.ValidationError):
        validate({}, core_schema)  # check on 'required'

    document = {
        'models': [{'name': 'A', 'attrs': [{'x_attr': {'name': 'x', 'value': 1}}]}],
        'categories': [{'name': 'K', 'models': ['A', 'B']}]
    }
    validate(document, core_schema)

    with pytest.raises(AssertionError):
        common.validate_transport(document)


def test_categories(core_schema):
    update_schema(core_schema, 'categories')

    validate([], core_schema)
    validate([{'name': 'K', 'models': []}], core_schema)

    with pytest.raises(js.exceptions.ValidationError):
        document = [
            {'name': 'K', 'models': []},
            {'a': 'b'},
        ]
        validate(document, core_schema)  # check on 'additionalItems'

    with pytest.raises(js.exceptions.ValidationError):
        document = [
            {'name': 'K', 'models': []},
            {'name': 'K', 'models': []},
        ]
        validate(document, core_schema)  # check on 'uniqueItems'

    # but it does not guaranty uniquenesses in the following case!
    # with pytest.raises(js.exceptions.ValidationError):
    #     document = [
    #         {'name': 'K', 'models': []},
    #         {'name': 'K', 'models': ['A', 'B']},
    #     ]
    #     validate(document, core_schema)  # check on 'uniqueItems'


def test_category(core_schema):
    update_schema(core_schema, 'category')

    validate({'name': 'K', 'models': []}, core_schema)
    validate({'name': 'K', 'models': ['A', 'B']}, core_schema)

    with pytest.raises(js.exceptions.ValidationError):
        validate({}, core_schema)  # check on 'required'

    with pytest.raises(js.exceptions.ValidationError):
        document = {'name': 'K', 'models': [], 'a': 'b'}
        validate(document, core_schema)  # check on 'additionalProperties'


def test_names(core_schema):
    update_schema(core_schema, 'names')

    validate([], core_schema)
    validate(['A'], core_schema)
    validate(['A', 'B'], core_schema)

    with pytest.raises(js.exceptions.ValidationError):
        validate([1], core_schema)  # check on 'additionalItems'

    with pytest.raises(js.exceptions.ValidationError):
        validate(['A', 1], core_schema)  # check on 'additionalItems'

    with pytest.raises(js.exceptions.ValidationError):
        validate(['A', 'A'], core_schema)  # check on 'uniqueItems'


def test_models(core_schema):
    update_schema(core_schema, 'models')

    document = [{'name': 'A'}]
    validate(document, core_schema)

    with pytest.raises(js.exceptions.ValidationError):
        document = {'a': 'b'}
        validate(document, core_schema)  # check on 'additionalItems'

    with pytest.raises(js.exceptions.ValidationError):
        document = [
            {'name': 'A', 'attrs': [{'x_attr': {'name': 'x', 'value': 1}}]},
            {'name': 'A'},
        ]
        validate(document, core_schema)  # check on 'uniqueItems'


def test_model(core_schema):
    update_schema(core_schema, 'model')

    document = {'name': 'A'}
    validate(document, core_schema)

    document = {'name': 'A', 'attrs': []}
    validate(document, core_schema)

    with pytest.raises(js.exceptions.ValidationError):
        document = {'attrs': []}
        validate(document, core_schema)  # check on 'required'

    with pytest.raises(js.exceptions.ValidationError):
        document = {'a': 'b'}
        validate(document, core_schema)  # check on 'additionalItems'

    document = {'name': 'A', 'attrs': [
        {'x_attr': {'name': 'x', 'value': 1}},
        {'y_attr': {'name': 'y', 'value': '1'}},
    ]}
    validate(document, core_schema)


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
