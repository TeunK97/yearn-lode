import pytest
from brownie import config
from brownie import Contract


@pytest.fixture
def gov(accounts):
    yield accounts.at("0xFEB4acf3df3cDEA7399794D0869ef76A6EfAff52", force=True)


@pytest.fixture
def user(accounts):
    yield accounts[0]


@pytest.fixture
def rewards(accounts):
    yield accounts[1]


@pytest.fixture
def guardian(accounts):
    yield accounts[2]


@pytest.fixture
def management(accounts):
    yield accounts[3]


@pytest.fixture
def strategist(accounts):
    yield accounts[4]


@pytest.fixture
def keeper(accounts):
    yield accounts[5]


@pytest.fixture
def want():
    token_address = "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8"  # this should be the address of the ERC-20 used by the strategy/vault (DAI)
    yield Contract.from_explorer(token_address)

@pytest.fixture
def weth():
    token_address = "0x82af49447d8a07e3bd95bd0d56f35241523fbab1"
    yield Contract.from_explorer(token_address)

@pytest.fixture
def ctoken():
    token_address = "0x5E3F2AbaECB51A182f05b4b7c0f7a5da1942De90"
    yield Contract.from_explorer(token_address)


@pytest.fixture
def amount(accounts, want, user):
    amount = 1000000 * 10 ** want.decimals()
    # In order to get some funds for the token you are about to use,
    # it impersonate an exchange address to use it's funds.
    usdc_whale = accounts.at('0x62383739d68dd0f844103db8dfb05a7eded5bbe6', force=True)
    want.transfer(user.address, (1000000 * 10 ** want.decimals()), {"from": usdc_whale})
    yield amount


@pytest.fixture
def weth():
    token_address = "0x82af49447d8a07e3bd95bd0d56f35241523fbab1"
    yield Contract.from_explorer(token_address)


@pytest.fixture
def weth_amout(user, weth):
    weth_amout = 10 ** weth.decimals()
    user.transfer(weth, weth_amout)
    yield weth_amout


@pytest.fixture
def vault(pm, gov, rewards, guardian, management, want):
    Vault = pm(config["dependencies"][0]).Vault
    vault = guardian.deploy(Vault)
    vault.initialize(want, gov, rewards, "Vault TEST", "VLT", guardian, management)
    vault.setDepositLimit(2 ** 256 - 1, {"from": gov})
    vault.setManagement(management, {"from": gov})
    yield vault


@pytest.fixture
def strategy(strategist, keeper, vault, Strategy, gov):
    strategy = strategist.deploy(Strategy, vault)
    strategy.setKeeper(keeper)
    vault.addStrategy(strategy, 10_000, 0, 2 ** 256 - 1, 1_000, {"from": gov})
    yield strategy


@pytest.fixture(scope="session")
def RELATIVE_APPROX():
    yield 1e-5
