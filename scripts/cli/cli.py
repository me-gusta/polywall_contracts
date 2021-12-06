from typing import Union

from brownie.network.account import LocalAccount

from scripts.cli.core.constants import LINE_LENGTH, LINE_PRICE, MAX_LINES_PER_TX
from scripts.cli.core.io import read_file_lines, print_wall_lines
from scripts.cli.core.pure import make_lines_for_tx, ensure_str_lengths

from brownie import *

from scripts.cli.core.my_types import PolyWallLine
from scripts.cli.ext.chunk import chunk
from scripts.cli.ext.cool_print import PrintColor, cprint, print_func_with_args


@print_func_with_args
def print_wall(from_uid: int = 0,
               amount: int = 20):
    """
    :param from_uid: ID of the first line to print
    :param amount: amount of lines to print
    :return:
    """
    assert amount > 0, 'Negative or null amount of lines requested'
    wall = PolyWall[-1]
    print_wall_lines(
        [PolyWallLine(*x) for x in wall.getLines(from_uid, amount)]
    )


@print_func_with_args
def deploy(account_slug: Union[str, LocalAccount], publish_source=False) -> Contract:
    """
    :param account_slug: name of your account
    """
    owner = accounts.load(account_slug)

    wall: Contract = PolyWall.deploy(
        LINE_LENGTH,
        Wei(f'{LINE_PRICE} ether'),
        {'from': owner},
        publish_source=True
    )

    cprint(PrintColor.PINK, f'PolyWall.sol is deployed on: {wall.address}')
    cprint(PrintColor.PINK, f'Line Price: {wall.LINE_PRICE() / (10 ** 18)} ether')
    return wall


@print_func_with_args
def withdraw(wall_address,
             account_slug: str):
    """
    :param wall_address: address of the PolyWall
    :param account_slug: name of your account
    """
    user = accounts.load(account_slug)
    wall = PolyWall.at(wall_address)
    cprint(PrintColor.PINK, f'Withdrawing {wall.pendingMatic(user.address)} MATIC')

    wall.withdraw({'from': user})

    cprint(PrintColor.PINK, f'User balance: {user.balance()}')
    return user


@print_func_with_args
def upload_file(wall_address: str,
                account_slug: Union[str, LocalAccount],
                file_name: str,
                from_uid: int):
    """
    :param wall_address: address of the PolyWall
    :param account_slug: name of your account or an instance of LocalAccount
    :param file_name: name of the desired file
    :param from_uid: ID of the line from which start uploading
    """
    cprint(PrintColor.PINK, f'Uploading file {file_name}')
    user = accounts.load(account_slug) if type(account_slug) == str else account_slug

    wall = PolyWall.at(wall_address)

    lines_for_tx = make_lines_for_tx(
        ensure_str_lengths(read_file_lines(file_name), LINE_LENGTH),
        MAX_LINES_PER_TX,
        from_uid
    )

    cprint(PrintColor.PINK, f'This will require {len(lines_for_tx)} transactions')

    line_price = wall.LINE_PRICE()
    for lines, uids in lines_for_tx:
        price = sum([PolyWallLine(*x).edits for x in wall.getLinesUnordered(uids)]) * line_price
        wall.uploadLines(lines, uids, {'from': user, 'value': price})


@print_func_with_args
def batch_upload_files(wall_address: str,
                       account_slug: str,
                       *args):
    """
    :param wall_address: address of the PolyWall
    :param account_slug: name of your account
    :param args: pairs of filename and start_uid. Example: 'readme.txt', 124325, 'second.txt', 5000
    :return:
    """
    chunked = chunk(args, 2)
    account = accounts.load(account_slug)
    [upload_file(wall_address, account, filename, start_uid) for filename, start_uid in chunked]


if __name__ == '__main__':
    batch_upload_files('asd',
                       'asfasf', 124124, 'safas', 4125)
