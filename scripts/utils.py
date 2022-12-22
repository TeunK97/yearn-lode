from pathlib import Path

from brownie import accounts, config, network, project, web3, Contract, Vault, Registry
from eth_utils import is_checksum_address
import click

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "arbitrum-fork"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-app"]
TESTNET =["goerli"]


# Vault = project.load(Path.home() / ".brownie" / "packages" / config["dependencies"][0]).Vault
# target token is now USDC. 
WANT = "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8"

def get_address(msg: str, default: str = None) -> str:
    val = click.prompt(msg, default=default)
    # Keep asking user for click.prompt until it passes
    while True:
        if is_checksum_address(val):
            return val
        elif addr := web3.ens.address(val):
            click.echo(f"Found ENS '{val}' [{addr}]")
            return addr
        click.echo(
            f"I'm sorry, but '{val}' is not a checksummed address or valid ENS record"
        )
        # NOTE: Only display default once
        val = click.prompt(msg)


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in TESTNET:
        return accounts.load("goerli_dev_1")
    if network.show_active() in FORKED_LOCAL_ENVIRONMENTS or LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]


def deploy_mock_vault():
    if network.show_active() == "arbitrum-fork":
        registry = Contract.from_explorer("0x3199437193625dccd6f9c9e98bdf93582200eb1f")
        # registry = Registry.at("0x3199437193625dccd6f9c9e98bdf93582200eb1f")
    else:
        print("Check network and/or include new registry.")
    token = Contract.from_explorer(WANT)
    deployer = get_account()

    gov = deployer.address
    rewards = get_account(index=2).address
    manager = deployer.address
    guardian = deployer.address
    name = "Vault X"
    symbol = "VLTX"
    click.echo(
        f"""
    Vault Deployment Parameters
     token address: {token.address}
      token symbol: {token.symbol}
        governance: {gov}
        management: {manager}
           rewards: {rewards}
          guardian: {guardian}
              name: '{name}'
            symbol: '{symbol}'
    """
    )
    vault = Vault.deploy({"from": deployer})
    vault.initialize(token, gov, rewards, name, symbol, guardian, manager)
    print(f"new vault deployed at {vault.address}")
    return vault