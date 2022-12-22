from scripts.utils import get_account
from brownie import Contract, accounts, web3, chain, Registry

# random constants
dev = get_account()
usdc_whale = accounts.at('0x62383739d68dd0f844103db8dfb05a7eded5bbe6', force=True)
WANT_token = Contract.from_explorer("0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8")
MASTERCHEF_address = "0x4Ce0C8C8944205C0A134ef37A772ceEE327B4c11"
RESERVOIR_address = "0x941a4EE8a96e0EEd086D5853c3661Bc4f2357ef2"
ibWANT_address = "0x5E3F2AbaECB51A182f05b4b7c0f7a5da1942De90"
UNITROLLER_address = "0x8f2354F9464514eFDAe441314b8325E97Bf96cdc"
ibWANT_token = Contract.from_explorer(ibWANT_address)
MASTERCHEF_contract = Contract.from_explorer(MASTERCHEF_address)
LODE_token = Contract.from_explorer("0xF19547f9ED24aA66b03c3a552D181Ae334FBb8DB")
UNITROLLER_contract = Contract.from_explorer("0x8f2354F9464514eFDAe441314b8325E97Bf96cdc")


## LODESTARCHEF IS FOR LP INCENTIVES.

def main():
    tx = WANT_token.transfer(dev.address, (1000000 * 10 ** WANT_token.decimals()), {"from": usdc_whale})
    tx.wait(1)
    print("USDC from whale to dev transferred")
    balance = WANT_token.balanceOf(dev.address)
    WANT_token.approve(ibWANT_token.address, balance, {"from":dev})
    print("Tokens approved")
    ibWANT_token.mint(balance, {"from":dev})
    tx.wait(1)
    print("Tokens minted")
    print(f"balance at block {web3.eth.block_number} is {ibWANT_token.balanceOf(dev.address)} tokens")
    chain.mine(5000)
    print(f"Now, 150 blocks further, at block {web3.eth.block_number} the balance is {ibWANT_token.balanceOf(dev.address)}")
    print("_____________________________")
    print("Check rewards using compAccrued")
    print(f"Using COMPACCRUED we have: {UNITROLLER_contract.compAccrued(dev.address)} outstanding rewards")
    print(f"Using COMPRECEIVABLE we have {UNITROLLER_contract.compReceivable(dev.address)} outstanding rewards")
    UNITROLLER_contract.updateContributorRewards(dev.address, {"from":dev})
    tx.wait(1)
    print("_____________________________")
    print("CHECKING AGAIN AFTER UPDATING")
    print(f"Using COMPACCRUED we have: {UNITROLLER_contract.compAccrued(dev.address)} outstanding rewards")
    print(f"Using COMPRECEIVABLE we have {UNITROLLER_contract.compReceivable(dev.address)} outstanding rewards")
    
    print("Claiming the tokens:")
    UNITROLLER_contract.claimComp(dev.address, [ibWANT_token.address], {"from":dev})
    tx.wait(1)
    print(f"Nice, we have now {LODE_token.balanceOf(dev.address)} in our wallet")



       
    



