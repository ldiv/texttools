from dataclasses import dataclass
from typing import Dict, List, Tuple, Callable


@dataclass
class Options:
    multiline: bool = True


class InvalidArgument(Exception):
    """The parameter name passed to the processor does not exist in the transform callback"""


class TextProcessor:
    def __init__(self, name: str, callback: Callable, parameters: Dict, options: Options = None):
        self.name = name
        self.callback = callback
        self.parameters = parameters
        self.options = options

    def _is_kwarg(self, arg: str) -> bool:
        if "=" in arg:
            argument_name = arg[:arg.index("=")]
            if argument_name not in self.parameters:
                raise InvalidArgument
            return True
        return False

    def _parse_argument_value(self, value: str):
        if value == "True" or value == "False":
            value = bool(value)
        elif value.startswith("'"):
            value = value.strip("'")
        elif value.startswith('"'):
            value = value.strip('"')
        elif value.isdigit():
            value = int(value)
        return value

    def validate_arguments(self, arguments: List[str]) -> Tuple[List, Dict]:
        args = []
        kwargs = {}
        for arg in arguments:
            if self._is_kwarg(arg):
                argument_name = arg[:arg.index("=")]
                argument_value = arg[arg.index("=")+1:]
                kwargs[argument_name] = self._parse_argument_value(argument_value)
            else:
                args.append(self._parse_argument_value(arg))
        return args, kwargs

    def __call__(self, text: str, arguments: List) -> str:
        args, kwargs = self.validate_arguments(arguments)
        if self.options and self.options.multiline:
            return "\n".join([self.callback(line, *args, **kwargs) for line in text.split("\n")])
        return str(self.callback(text, *args, **kwargs))
