"""
create json format
"""
from typing import Any, Dict

Source = {'a': ['x', 'y'], 'b': ['z'], 'c': []}
JSDocument = Dict[str, Any]


def handler_json(source: JSDocument) -> Any:
    """print and return json format"""
    mas = []
    print(list(source.keys()))
    for key in source.keys():
        mas.append({'name': key, 'attrs': source.get(key)})
    categories = [{'name': 'viscosity', 'models': list(source.keys())}]
    models = {'models': mas, 'categories': categories}
    main = {'transport': models}
    return main
