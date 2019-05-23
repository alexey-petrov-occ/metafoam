import pytest

import jsonschema as js
import python_jsonschema_objects as pjs

import metafoam
from metafoam import common
from metafoam.common import validate, definition2schema


@pytest.fixture
def core_document():
    return {'transport': {
        'models': [
            {'name': 'a', 'attrs': [
                {'x_attr': {'name': 'x', 'value': 1}},
                {'y_type': {'name': 'y', 'value': '1'}},
            ]},
            {'name': 'b', 'attrs': [
                {'z_attr': {'name': 'z', 'value': False}},
            ]},
            {'name': 'c', 'attrs': []},
        ],
        'categories': [
            {'name': 'K', 'models': ['b']},
            {'name': 'L', 'models': ['a', 'c']},
        ],
    }}


@pytest.fixture
def solver_document():
    return {'transport': 'K'}


@pytest.fixture
def transport(core_schema, core_document, solver_schema, solver_document):
    definition2schema(core_schema, 'core')
    definition2schema(solver_schema, 'solver')

    core = metafoam.Core(core_document, core_schema)
    solver = metafoam.Solver(solver_document, solver_schema, core)

    return solver.transport


def test_transport_attrs(transport):
    transport.category = 'L'
    transport.model = 'a'

    assert transport.attrs == ['x', 'y']

    instance = transport.attr('y')
    assert instance.value == '1'

    instance.value = 'abc'
    assert instance.value == 'abc'

    with pytest.raises(pjs.validators.ValidationError):
        instance.value = 1
    assert instance.value == 'abc'


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
            'x-type': {'title': 'x_type', 'type': 'object', 'properties': {
                'value': {'type': 'number'},
                'name': {'type': 'string'},
            }, 'required': ['name'], 'additionalProperties': False},
            'x-attr': {'title': 'x_attr', 'type': 'object', 'properties': {
              'x_attr': {'$ref': '#/definitions/x-type'},
            }, 'required': ['x_attr'], 'additionalProperties': False},

            'y-type': {'title': 'y_type', 'type': 'object', 'properties': {
                'value': {'type': 'string'},
                'name': {'type': 'string'},
            }, 'required': ['name'], 'additionalProperties': False},
            'y-attr': {'title': 'y_attr', 'type': 'object', 'properties': {
              'y_type': {'$ref': '#/definitions/y-type'},
            }, 'required': ['y_type'], 'additionalProperties': False},

            'z-type': {'title': 'ZType', 'type': 'object', 'properties': {
                'value': {'type': 'boolean'},
                'name': {'type': 'string'},
            }, 'required': ['name'], 'additionalProperties': False},
            'z-attr': {'title': 'ZAttr', 'type': 'object', 'properties': {
              'z_attr': {'$ref': '#/definitions/z-type'},
            }, 'required': ['z_attr'], 'additionalProperties': False},

            'attrs': {'title': 'TAttrs', 'type': 'array', 'items': {'oneOf': [
                {'$ref': '#/definitions/x-attr'},
                {'$ref': '#/definitions/y-attr'},
                {'$ref': '#/definitions/z-attr'},
            ]}, 'additionalItems': False, 'uniqueItems': True},

            'model': {'type': 'object', 'properties': {
                'name': {'type': 'string'},
                'attrs': {'$ref': '#/definitions/attrs'},
            }, 'required': ['name'], 'additionalProperties': False},
            'models': {'type': 'array', 'items': {'oneOf': [
                {'$ref': '#/definitions/model'},
            ]}, 'additionalItems': False, 'uniqueItems': True},

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

            'core': {'type': 'object', 'properties': {
                'transport': {'$ref': '#/definitions/transport'},
            }, 'additionalProperties': False},
        },
    }


def test_solver_introspection(core_schema, solver_schema):
    definition2schema(core_schema, 'core')
    definition2schema(solver_schema, 'solver')

    with pytest.raises(js.exceptions.ValidationError):
        document = {'transport': {
            'models': [
                {'name': 'a', 'attrs': [
                    {'d_attr': {'name': 'd', 'value': False}},
                ]},
            ],
        }}
        metafoam.Core(document, core_schema)  # check on 'additionalProperties'

    document = {'transport': {
        'models': [
            {'name': 'a', 'attrs': [
                {'x_attr': {'name': 'x', 'value': 1}},
                {'y_type': {'name': 'y', 'value': '1'}},
            ]},
            {'name': 'b', 'attrs': [
                {'z_attr': {'name': 'z', 'value': False}},
            ]},
            {'name': 'c', 'attrs': []},
        ],
        'categories': [
            {'name': 'K', 'models': ['b']},
            {'name': 'L', 'models': ['a', 'c']},
        ],
    }}
    core = metafoam.Core(document, core_schema)

    # solver 'transport' should be in core 'transport/categories'
    with pytest.raises(AssertionError):
        document = {'transport': 'M'}
        metafoam.Solver(document, solver_schema, core)

    document = {'transport': 'K'}
    solver = metafoam.Solver(document, solver_schema, core)

    transport = solver.transport
    assert transport.category == 'K'

    assert transport.model == ''
    with pytest.raises(AssertionError):
        transport.attrs

    transport.model = 'b'
    assert transport.model == 'b'

    with pytest.raises(AssertionError):
        transport.model = 'a'

    assert transport.attrs == ['z']

    transport.category = 'L'
    assert transport.category == 'L'

    with pytest.raises(AssertionError):
        transport.category = 'M'
    assert transport.category == 'L'

    assert transport.model == ''


def test_solver(solver_schema):
    definition2schema(solver_schema, 'solver')

    validate({}, solver_schema)

    validate({'transport': 'A'}, solver_schema)

    with pytest.raises(js.exceptions.ValidationError):
        validate({'a': 'b'}, solver_schema)  # check on 'additionalProperties'


def test_core(core_schema):
    definition2schema(core_schema, 'core')

    validate({}, core_schema)

    validate({'transport': {'models': [], 'categories': []}}, core_schema)

    with pytest.raises(js.exceptions.ValidationError):
        validate({'a': 'b'}, core_schema)  # check on 'additionalProperties'

    document = {'transport': {
        'models': [{'name': 'A', 'attrs': [{'x_attr': {'name': 'x', 'value': 1}}]}],
        'categories': [{'name': 'K', 'models': ['A', 'B']}],
    }}
    validate(document, core_schema)

    with pytest.raises(AssertionError):
        common.validate_model(document, core_schema)


def test_transport(core_schema):
    definition2schema(core_schema, 'transport')

    validate({'models': [], 'categories': []}, core_schema)

    with pytest.raises(js.exceptions.ValidationError):
        validate({}, core_schema)  # check on 'required'

    document = {
        'models': [{'name': 'A', 'attrs': [
            {'x_attr': {'name': 'x1', 'value': 1}},
            {'x_attr': {'name': 'x2'}},
        ]}],
        'categories': [{'name': 'K', 'models': ['A', 'B']}]
    }
    validate(document, core_schema)

    with pytest.raises(AssertionError):
        common.validate_transport(document)

    model2attrs = common.models(document)
    attrs = model2attrs['A']

    names = common.attrs2names(attrs)
    assert set(('x1', 'x2')) == set(names)


def test_categories(core_schema):
    definition2schema(core_schema, 'categories')

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
    definition2schema(core_schema, 'category')

    validate({'name': 'K', 'models': []}, core_schema)
    validate({'name': 'K', 'models': ['A', 'B']}, core_schema)

    with pytest.raises(js.exceptions.ValidationError):
        validate({}, core_schema)  # check on 'required'

    with pytest.raises(js.exceptions.ValidationError):
        document = {'name': 'K', 'models': [], 'a': 'b'}
        validate(document, core_schema)  # check on 'additionalProperties'


def test_names(core_schema):
    definition2schema(core_schema, 'names')

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
    definition2schema(core_schema, 'models')

    document = [{'name': 'A'}]
    validate(document, core_schema)

    with pytest.raises(js.exceptions.ValidationError):
        document = {'a': 'b'}
        validate(document, core_schema)  # check on 'additionalItems'

    with pytest.raises(js.exceptions.ValidationError):
        document = [
            {'name': 'A'},
            {'name': 'A'},
        ]
        validate(document, core_schema)  # check on 'uniqueItems'

    # but it does not guaranty uniquenesses in the following case!
    # with pytest.raises(js.exceptions.ValidationError):
    #     document = [
    #         {'name': 'A', 'attrs': [{'x_attr': {'name': 'x', 'value': 1}}]},
    #         {'name': 'A'},
    #     ]
    #     validate(document, core_schema)  # check on 'uniqueItems'

    document = [
        {'name': 'A'},
        {'name': 'B'},
    ]
    validate(document, core_schema)


def test_model(core_schema):
    definition2schema(core_schema, 'model')

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

    with pytest.raises(js.exceptions.ValidationError):
        document = {'name': 'A', 'attrs': [
            {'a_attr': {'name': 'a', 'value': 1}},
        ]}
        validate(document, core_schema)  # check on 'additionalItems'

    document = {'name': 'A', 'attrs': [
        {'x_attr': {'name': 'x', 'value': 1}},
        {'y_type': {'name': 'y', 'value': '1'}},
        {'z_attr': {'name': 'z', 'value': False}},
    ]}
    validate(document, core_schema)


def test_attrs(core_schema):
    definition2schema(core_schema, 'attrs')

    document = [
        {'x_attr': {'name': 'x', 'value': 1}},
        {'y_type': {'name': 'y', 'value': '1'}},
    ]
    validate(document, core_schema)

    with pytest.raises(js.exceptions.ValidationError):
        document = [
            {'x_attr': {'name': 'x', 'value': 1}},
            {'x_attr': {'name': 'x', 'value': 1}},
        ]
        validate(document, core_schema)  # check on 'uniqueItems'

    document = [
        {'y_type': {'name': 'y', 'value': '1'}},
        {'y_type': {'name': 'y', 'value': '2'}},
    ]
    validate(document, core_schema)  # check on 'uniqueItems'

    with pytest.raises(js.exceptions.ValidationError):
        validate([{'a': 'b'}], core_schema)  # check on 'additionalItems'


def test_z_attr(core_schema):
    definition2schema(core_schema, 'z-attr')

    validate({'z_attr': {'name': 'z', 'value': False}}, core_schema)

    with pytest.raises(js.exceptions.ValidationError):
        validate({'z_attr': {'name': 'z', 'value': 1}}, core_schema)


def test_x_attr(core_schema):
    definition2schema(core_schema, 'x-attr')

    validate({'x_attr': {'name': 'x', 'value': 1}}, core_schema)

    validate({'x_attr': {'name': 'x'}}, core_schema)

    with pytest.raises(js.exceptions.ValidationError):
        validate({'x_attr': {'value': 1}}, core_schema)

    with pytest.raises(js.exceptions.ValidationError):
        validate({'x_attr': {}}, core_schema)

    builder = pjs.ObjectBuilder(core_schema)
    ns = builder.build_classes(strict=True, named_only=False, standardize_names=False)

    with pytest.raises(pjs.validators.ValidationError):
        ns.x_type()

    x = ns.x_type(name='x1')
    assert x.name == 'x1'
    assert x.value is None

    with pytest.raises(pjs.validators.ValidationError):
        x.dummy = 1

    with pytest.raises(pjs.validators.ValidationError):
        x.value = 'txt'

    x.value = 10
    assert x.value == 10
