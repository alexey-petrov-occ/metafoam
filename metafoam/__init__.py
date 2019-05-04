from typing import Dict

JSDocument = Dict

def categories(model: JSDocument) -> Dict:
    return dict((item['name'], item['models']) for item in model['categories'])
