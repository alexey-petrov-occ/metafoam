"""
create json format
"""
Source = {'a': ['x', 'y'], 'b': ['z'], 'c': []}


def handler_json(source):
    """print and return json format"""
    mas = []
    print(list(source.keys()))
    for key in source.keys():
        mas.append({'name': key, 'attrs': source.get(key)})
    categories = [{'name': 'viscosity', 'models': list(source.keys())}]
    models = {'models': mas, 'categories': categories}
    main = {'transport': models}
    print(main)
    return main
