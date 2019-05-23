"""Defines Core metamodel for OpenFOAM
"""
import copy
import typing

import python_jsonschema_objects as pjs

from .common import JSDocument, JSSchema, Name, Entity2Attrs, Models

from .common import categories, models, validate_model


class Core:
    "Provides semantic level validation and programming API for an OpenFOAM core"
    __slots__ = ('_document', '_namespace')

    def __init__(self, document: JSDocument, schema: JSSchema):
        validate_model(document, schema)
        self._document = document

        builder = pjs.ObjectBuilder(schema)
        self._namespace = builder.build_classes(strict=True, named_only=False, standardize_names=False)

    @property
    def document(self) -> JSDocument:
        "Returns initial document"
        return copy.copy(self._document)

    def categories(self, name: Name) -> Entity2Attrs:
        "Extracts 'categories' for the given OpenFOAM model 'name'"
        return categories(self._document[name])

    def models(self, name: Name) -> Models:
        "Extracts 'models' for the given OpenFOAM model 'name'"
        return models(self._document[name])

    def namespace(self) -> typing.Any:
        "Returns 'definitions' namespace"
        return self._namespace
