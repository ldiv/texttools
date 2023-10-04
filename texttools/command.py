import re
import inspect
from collections import namedtuple
from typing import List, Callable, Tuple

from .transforms import chainables, scalars
from .processor import TextProcessor, Options


CHAIN_SYMBOL = "->"
COMMAND_PATTERN = r"(\w+)(?:\((.*)\))*"
WORD_MODE_PARAM = "operate_on_word"

Transform = namedtuple("Transform", "name arguments")


class InvalidCommand(Exception):
    pass


def _parse_command_string(command_string: str) -> List[Transform]:
    transforms = []

    for operation in command_string.split(CHAIN_SYMBOL):
        if not (m := re.match(COMMAND_PATTERN, operation)):
            raise InvalidCommand(f"Error parsing operation: {operation}")
        function_name, arguments = m.groups()
        arguments = m.groups()[1].split(",") if arguments else []
        transforms.append(Transform(function_name, arguments))

    return transforms


def _is_chainable(transform: Transform):
    return transform.name in chainables


def _is_scalar(transform: Transform):
    return transform.name in scalars


def _is_valid_transform(transform: Transform):
    return _is_scalar(transform) or _is_chainable(transform)


def validate_transforms(transforms: List[Transform]) -> List[Tuple[Transform, Callable]]:
    if not transforms:
        raise ValueError
    # First transform can be scalar or chainable
    if not _is_valid_transform(transforms[0]):
        raise InvalidCommand(f"Not a valid operation: {transforms[0]}")

    callbacks = []
    if _is_chainable(transforms[0]):
        callbacks.append(chainables[transforms[0].name])
    else:
        callbacks.append(scalars[transforms[0].name])

    # The rest can only be chainables
    for i, transform in enumerate(transforms[1:]):
        if transform.name not in chainables:
            raise InvalidCommand(f"Operation is not chainable: {transform}")
        callbacks.append(chainables[transform.name])

    return list(zip(transforms, callbacks))


def run_command(text, command_string, multiline=False, word_mode=False):
    transforms = _parse_command_string(command_string)
    options = Options(multiline=multiline)

    processors = []
    for transform, fn in validate_transforms(transforms):
        fn_parameters = dict(inspect.signature(fn).parameters)
        if ("w" in transform.arguments or word_mode) and WORD_MODE_PARAM in fn_parameters:
            transform.arguments[transform.arguments.index("w")] = f"{WORD_MODE_PARAM}=True"
        processors.append(
            (TextProcessor(transform.name, fn, fn_parameters, options), transform.arguments)
        )

    result = text
    for processor, arguments in processors:
        result = processor(result, arguments)

    return result
