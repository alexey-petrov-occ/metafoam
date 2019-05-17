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
        },
        'title': 'test', 'type': 'object', 'properties': {
            'x_attr': {'$ref': '#/definitions/x-type'},
        },
    }


def test(core_schema):
    js.validate({'x_attr': {'name': 'x', 'value': 1}}, core_schema)

    js.validate({'x_attr': {'name': 'x'}}, core_schema)

    with pytest.raises(js.exceptions.ValidationError):
        js.validate({'x_attr': {'value': 1}}, core_schema)

    with pytest.raises(js.exceptions.ValidationError):
        js.validate({'x_attr': {}}, core_schema)

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
