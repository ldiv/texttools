import random
import re
import string
from base64 import b64decode, b64encode
from string import ascii_letters
from typing import Callable
from urllib.parse import quote_plus, quote, unquote_plus, unquote


WORD = r"\w"  # [a-z][A-Z][0-9][_-]


chainables = {}
scalars = {}


class FunctionNotChainable(Exception):
    ...


def chainable(fn: Callable) -> Callable:
    """ Decorator to load chainable functions in a namespace """
    chainables[fn.__name__] = fn
    return fn


def scalar(fn: Callable) -> Callable:
    """ Decorator to load non-chainable functions in a namespace """
    scalars[fn.__name__] = fn
    return fn


@scalar
def count_words(text: str, word_pattern=WORD) -> int:
    return len(text.split(" "))


@scalar
def count_lines(text: str) -> int:
    return len(text.splitlines())


@scalar
def count_characters(text: str, exclude_spaces: bool = False, exclude_non_printable=True) -> int:
    # TODO: Need to handle non-printable characters
    return len(re.sub(r"\s", "", text)) if exclude_spaces else len(text)


@chainable
def rot13(text: str) -> str:
    mapping = str.maketrans(
        string.ascii_uppercase + string.ascii_lowercase,
        string.ascii_uppercase[13:] + string.ascii_uppercase[:13] +
        string.ascii_lowercase[13:] + string.ascii_lowercase[:13]
    )
    return text.translate(mapping)


@chainable
def url_encode(text: str, space_as_plus=True) -> str:
    return quote_plus(text) if space_as_plus else quote(text)


@chainable
def url_decode(text: str, space_as_plus=True) -> str:
    return unquote_plus(text) if space_as_plus else unquote(text)


@chainable
def base64_encode(text: str, trim_whitespace=True) -> str:
    if trim_whitespace:
        return b64encode(text.strip().encode("utf-8")).decode("utf-8")
    return b64encode(text.encode("utf-8")).decode("utf-8")


@chainable
def base64_decode(text: str, trim_whitespace=True) -> str:
    if trim_whitespace:
        return b64decode(text.strip()).decode("utf-8")
    return b64decode(text).decode("utf-8")


def generate_password(length: int = 14, exclude=None) -> str:
    letters = ascii_letters
    digits = range(10)
    metachar = ['!', '*', '@', '^', '-', '+', '%', '$', '~']

    min_num_of_letters = int(length * .6)
    num_of_letters = random.randint(min_num_of_letters, min_num_of_letters + 3)
    num_of_metachars = 2
    num_of_digits = length - min_num_of_letters - num_of_metachars

    password = random.choices(letters, k=num_of_letters) + \
               list(map(str, random.choices(digits, k=num_of_digits))) + \
               random.choices(metachar, k=num_of_metachars)
    random.shuffle(password)
    return "".join(password)


@chainable
def reverse(text: str, operate_on_word: bool = False) -> str:
    if operate_on_word:
        word_delimiter = " "
        return "\n".join([" ".join(re.split(word_delimiter, line)[::-1]) for line in text.split("\n")])
    return text[::-1]


@chainable
def replace(text: str, string_to_replace, replacement) -> str:
    return re.sub(string_to_replace, replacement, text)


@chainable
def add_before(text: str, string_to_add) -> str:
    return string_to_add + text


@chainable
def add_after(text: str, string_to_add) -> str:
    return text + string_to_add


@chainable
def trim(text: str, string_to_remove=None) -> str:
    if string_to_remove:
        return text.strip(text)
    return text.strip()


@chainable
def title_case(text: str) -> str:
    return text.capitalize()


@chainable
def lower_case(text: str) -> str:
    return text.lower()


@chainable
def upper_case(text: str) -> str:
    return text.upper()


@chainable
def sort(text: str, operate_on_word: bool = False) -> str:
    if operate_on_word:
        word_delimiter = " "
        return "\n".join([" ".join(sorted(re.split(word_delimiter, line))) for line in text.split("\n")])
    return "".join(sorted(text))


@chainable
def slugify(text: str) -> str:
    """ Lowercases text and coalesces spaces replacing them with an underscore """
    return re.sub(r"\s", "-", text.lower())


@chainable
def remove(text: str, string_to_remove: str) -> str:
    return replace(text, string_to_remove, "")
