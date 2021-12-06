from typing import List

from brownie import Wei
from brownie.network.account import Account
from brownie.network.contract import ContractContainer

from scripts.cli.core import constants
from scripts.cli.core.pure import wei_to_eth


def test_init(TheWall: ContractContainer, accounts: List[Account]):
    owner = accounts[0]
    user1 = accounts[1]

    # Deploy
    wall = TheWall.deploy(constants.LINE_LENGTH,
                          Wei(f'{constants.LINE_PRICE} ether'),
                          {'from': owner})

    # wall_print_lines(wall, 0, 20)

    # Upload lines
    wall.uploadLines(
        ["AAAAAA dolor sit amet, consectetur adipiscing elit.", "Yo nigger"],
        [1, 2],
        {'from': owner, 'value': Wei('0.002 ether'), 'gas_limit': 1_000_000},
    )

    wall.uploadLines(
        ["AAAAAA dolor sit amet, consectetur adipiscing elit.", "Yo nigger"],
        [1, 2],
        {'from': user1, 'value': Wei('0.004 ether'), 'gas_limit': 1_000_000},
    )
    print(f'Balance      = {wei_to_eth(wall.balance())}')
    assert wall.balance() == Wei('0.006 ether'), "Incorrect wall balance"

    # Withdraw funds
    print(f'Show balance = {wei_to_eth(wall.pendingMatic(owner.address))}')

    wall.withdraw({'from': owner})
    print(f'New balance  = {wei_to_eth(wall.balance())}')
    print()
    assert False
