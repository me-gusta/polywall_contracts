import inspect
from decimal import Decimal
from enum import Enum
from typing import Union, Dict, Any


class PrintColor(Enum):
    PINK = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def cprint(color: PrintColor, *args):
    print(color.value, *args, PrintColor.ENDC.value, sep='')


def cprint_fname(color: PrintColor, *args):
    # Be careful! This can incur heavy performance overhead
    print(f'{color.value}{inspect.stack()[1].function}: ', *args, PrintColor.ENDC.value, sep='')


def print_func_with_args(func):
    def wrapper(*args, **kwargs):
        cprint(PrintColor.PINK, f'Executing {func.__name__}')
        for i, arg in enumerate(args):
            cprint(PrintColor.CYAN, f'    {i}: {arg}')
        for k, v in kwargs.items():
            cprint(PrintColor.CYAN, f'    {k}: {v}')
        print()
        return func(*args, **kwargs)

    return wrapper


def printable_float(number: Union[Decimal, float]) -> str:
    return '{0:.10f}'.format(number)


def iter_obj(obj: Any, no_underscores=True, show_types=False) -> Dict[str, Any]:
    args = obj.__dir__()
    if no_underscores:
        args = [x for x in args if not x.startswith('_')]
    out = {}
    for arg in args:
        value = obj.__getattribute__(arg)
        if show_types:
            value = (type(value), value)
        out[arg] = value
    return out
