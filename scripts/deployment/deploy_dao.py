import json

from brownie import (
    ERC20CRV,
    GaugeController,
    LiquidityGauge,
    LiquidityGaugeReward,
    Minter,
    PoolProxy,
    VotingEscrow,
    accounts,
    history,
    Contract,
    FeeDistributor,
    chain
)

from . import deployment_config as config
# modify me prior to deployment on mainnet!
DEPLOYER = accounts.at("0x7EeAC6CDdbd1D0B8aF061742D41877D7F707289a", force=True)

OWNER_ADMIN = "0x5195858f396B11F8B11EDA1b0E90CC49D57CAa0c"
EMERGENCY_ADMIN = "0x397A7EC90bb4f0e89Ffd2Fb3269a3ef295d4f84A"


def live_part_one():
    admin, _ = config.get_live_admin()
    deploy_part_one(admin, config.REQUIRED_CONFIRMATIONS, config.DEPLOYMENTS_JSON)


def live_part_two():
    admin, _ = config.get_live_admin()
    with open(config.DEPLOYMENTS_JSON) as fp:
        deployments = json.load(fp)
    token = ERC20CRV.at(deployments["ERC20CRV"])
    voting_escrow = VotingEscrow.at(deployments["VotingEscrow"])

    deploy_part_two(
        admin, token, voting_escrow, config.REQUIRED_CONFIRMATIONS, config.DEPLOYMENTS_JSON
    )


def development():
    dev = get_admin()
    token, voting_escrow = deploy_part_one(dev)
    print(token, voting_escrow)
    # deploy_part_two(dev, token, voting_escrow)


def deploy_part_one(admin, confs=1, deployments_json=None):
    token = ERC20CRV.deploy("Curve DAO Token", "CRV", 18, {"from": admin, "required_confs": confs})
    voting_escrow = VotingEscrow.deploy(
        token,
        "Vote-escrowed CRV",
        "veCRV",
        "veCRV_1.0.0",
        {"from": admin, "required_confs": confs},
    )
    deployments = {
        "ERC20CRV": token.address,
        "VotingEscrow": voting_escrow.address,
    }
    if deployments_json is not None:
        with open(deployments_json, "w") as fp:
            json.dump(deployments, fp)
        print(f"Deployment addresses saved to {deployments_json}")

    return token, voting_escrow


def deploy_part_two(admin, token, voting_escrow, confs=1, deployments_json=None):

    deployments = {
        "ERC20CRV": token.address,
        "VotingEscrow": voting_escrow.address,
    }

    print(f"Deployment complete! Total gas used: {sum(i.gas_used for i in history)}")
    if deployments_json is not None:
        with open(deployments_json, "w") as fp:
            json.dump(deployments, fp)
        print(f"Deployment addresses saved to {deployments_json}")


def get_admin():
    print("Deploying on chain id:", chain.id)
    if chain.id == 5:  # if deploying to not locally
        dev = accounts.load('100')
    else:
        dev = accounts[0]
    print("deploying with account:", dev)
    return dev


def test():
    dev = get_admin()
    distributor = deploy_fee_distributor(dev)
    print(distributor)


# voting_escrow is goerli and fee_token is default ERC20
def deploy_fee_distributor(admin, voting_escrow="0xa5ade372ea523e407db1bd8d1d0cd3fbf5fee9d4", fee_token="0xb94f5916611df8a01c2804938ee17e291dbeaf81"):
    start_time = 1600300800
    distributor = FeeDistributor.deploy(
        voting_escrow,  # VotingEscrow
        start_time,
        Contract(fee_token),
        OWNER_ADMIN,
        EMERGENCY_ADMIN,
        {"from": admin},
    )
    return distributor
