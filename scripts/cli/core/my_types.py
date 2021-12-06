from dataclasses import dataclass

from scripts.cli.core.constants import LINE_LENGTH
from scripts.cli.core.pure import beautify_number


@dataclass
class PolyWallLine:
    uid: int
    _str: str
    edits: int = -1

    def __post_init__(self):

        if len(self._str) == 0:
            self._str = '×' * LINE_LENGTH
        elif len(self._str) <= LINE_LENGTH:
            self._str += ' ' * (LINE_LENGTH - len(self._str))
        else:
            raise ValueError(
                f'Unexpected line length from blockchain {len(self._str)}/{LINE_LENGTH}: {self._str}')

    def __repr__(self):
        return f'{beautify_number(self.uid)}|{self.edits}|{self._str}|'
