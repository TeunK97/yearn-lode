import brownie
from brownie import Contract, chain
import pytest

def test_deposit_and_withdrawal(user, want, amount, vault, strategy, RELATIVE_APPROX):
    user_balance_before = want.balanceOf(user.address)
    want.approve(vault.address, amount, {"from": user})
    vault.deposit(amount, {"from": user})
    assert want.balanceOf(vault.address) == amount
    chain.sleep(1)
    
    # after harvest, assets from vault are succesfully moved into the strategy
    # harvest function performed by strategist
    strategy.harvest()
    
    # check if assets are indeed in strategy
    assert pytest.approx(strategy.estimatedTotalAssets(), rel=RELATIVE_APPROX) == amount
   
    # tend()
    # tend also called by strategist
    # this function does not realize funds, but maximizes yield by reinvestment. 
    # it calls adjustfunction with vault.debtOutstanding() as args. adjustfunction in strat.sol
    strategy.tend()

    # withdrawal
    vault.withdraw({"from": user})
    assert (pytest.approx(want.balanceOf(user), rel=RELATIVE_APPROX) == user_balance_before)
    assert vault.address == user.address
