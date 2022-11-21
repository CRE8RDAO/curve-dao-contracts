import json

from brownie import (
    ERC20CRV,
    VotingEscrow,
    accounts,
    history,
    Contract,
    FeeDistributor,
    chain
)
# TODO: Need to make sure that admin are right.
from . import deployment_config as config
# modify me prior to deployment on mainnet!
DEPLOYER = accounts.at("0x7EeAC6CDdbd1D0B8aF061742D41877D7F707289a", force=True)

OWNER_ADMIN = "0x5195858f396B11F8B11EDA1b0E90CC49D57CAa0c"
EMERGENCY_ADMIN = "0x397A7EC90bb4f0e89Ffd2Fb3269a3ef295d4f84A"


def deploy_live():
    admin, _ = config.get_live_admin()
    deploy(admin, config.REQUIRED_CONFIRMATIONS, config.DEPLOYMENTS_JSON)


def development():
    dev = get_admin()
    deploy(dev)


def deploy(admin, confs=1, deployments_json=None):
    token = ERC20CRV.deploy("AmpliFi Test DAO Token", "testAGG", 18,
                            {"from": admin, "required_confs": confs})
    voting_escrow = VotingEscrow.deploy(
        token,
        "Vote-escrowed testAGG",
        "testLAGG",
        "testLAGG_1.0.0",
        "0x397A7EC90bb4f0e89Ffd2Fb3269a3ef295d4f84A",
        {"from": admin, "required_confs": confs},
    )

    start_time = 1600300800
    voting_escrow = "0xa5ade372ea523e407db1bd8d1d0cd3fbf5fee9d4"
    fee_token = "0xb94f5916611df8a01c2804938ee17e291dbeaf81"
    distributor = FeeDistributor.deploy(
        voting_escrow,  # VotingEscrow
        start_time,
        fee_token,
        OWNER_ADMIN,
        EMERGENCY_ADMIN,
        {"from": admin}
    )
    deployments = {
        "ERC20": token.address,
        "VotingEscrow": voting_escrow,
        "FeeDistributor": distributor.address
    }

    if deployments_json is not None:
        with open(deployments_json, "w") as fp:
            json.dump(deployments, fp)
        print(f"Deployment addresses saved to {deployments_json}")

    return token, voting_escrow, distributor


def get_admin():
    print("Deploying on chain id:", chain.id)
    if chain.id == 5:  # goerli
        dev = accounts.load('100')
    else:
        dev = accounts[0]
    print("deploying with account:", dev)
    return dev
