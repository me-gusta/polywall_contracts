from typing import List, Any, Tuple, Union


# TODO: simplify this type hint
def chunk(arr: Union[List[Any], Tuple[Any]], n: int):
    return [arr[i:i + n] for i in range(0, len(arr), n)]
