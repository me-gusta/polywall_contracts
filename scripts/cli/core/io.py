from pathlib import Path
from typing import List, Union

from scripts.cli.core.constants import FILES_DIR
from scripts.cli.core.my_types import PolyWallLine
from scripts.cli.ext.cool_print import PrintColor, cprint


def read_file_lines(filename: Union[str, Path]) -> List[str]:
    with open(FILES_DIR / filename, 'r', encoding='utf-8') as f:
        return f.read().splitlines()


def print_wall_lines(lines: List[PolyWallLine]) -> None:
    border_color = PrintColor.PINK

    cprint(border_color, '#' * 106)
    [print(line) for line in lines]
    cprint(border_color, '#' * 106)
