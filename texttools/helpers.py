import inspect

import transforms


def get_scalar_transforms():
    members = {name: value for name, value in inspect.getmembers(transforms)}
    chainables = members.get("chainables", [])
    scalars = []
    for name, value in members.items():
        if inspect.isfunction(value) and name not in chainables:
            scalars.append(value)
    ok=7

get_scalar_transforms()
