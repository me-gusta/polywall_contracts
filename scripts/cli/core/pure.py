from itertools import chain
from textwrap import wrap
from typing import List, Tuple

from web3 import Web3

from scripts.cli.ext.chunk import chunk


def beautify_number(x: int) -> str:
    x = str(x)
    return '0' + x if len(x) == 1 else x


def wei_to_eth(wei_amount: int):
    return Web3.fromWei(wei_amount, 'ether')


def ensure_str_lengths(list_str: List[str], line_length: int) -> List[str]:
    def wrap_or_empty(line: str):
        """By default wrap('') returns [] which can cause problems"""
        return wrap(line, line_length) if line else [" "]

    list_of_lists = [wrap_or_empty(x) for x in list_str]
    return [*chain.from_iterable(list_of_lists)]  # unwrap


def make_lines_for_tx(lines: List[str], lines_per_tx: int, start_uid: int) -> List[Tuple[List[str], List[int]]]:
    """Lines must be already of required length.
    Adds a list of uids for each list of lines.
    Output data may be used for transaction in PolyWall.uploadLines()"""

    def generate_uids(start_from: int, amount: int) -> List[int]:
        return [x for x in range(start_uid + start_from, start_uid + start_from + amount)]

    def make_lines_and_uids(start_from: int, lines: List[str]) -> Tuple[List[str], List[int]]:
        return lines, generate_uids(start_from * lines_per_tx, len(lines))

    lines_chunked: List[List[str]] = chunk(lines, lines_per_tx)

    return [make_lines_and_uids(i, lines) for i, lines in enumerate(lines_chunked)]
