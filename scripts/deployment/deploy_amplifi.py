import json

from brownie import (
    ERC20CRV,
    VotingEscrow,
    accounts,
    history,
    Contract,
    FeeDistributor,
    chain,
    network
)
# TODO: Need to make sure that admin are right.
from . import deployment_config as config
H = 3600
DAY = 86400
WEEK = 7 * DAY
MAXTIME = 126144000
TOL = 120 / WEEK
# modify me prior to deployment on mainnet!
DEPLOYER = accounts.at("0x7EeAC6CDdbd1D0B8aF061742D41877D7F707289a", force=True)

OWNER_ADMIN = "0x5195858f396B11F8B11EDA1b0E90CC49D57CAa0c"
EMERGENCY_ADMIN = "0x6A03fa1df243aBE7A46Cf943dE1B1E500285949c"


def deploy_live():
    admin, _ = config.get_live_admin()
    deploy_ve(admin, config.REQUIRED_CONFIRMATIONS, config.DEPLOYMENTS_JSON)


def development(enable_tests=False):
    admin = get_admin()
    token = deploy_mock_erc20(admin)
    _, voting_escrow, distributor = deploy(admin, token, token.address)
    if enable_tests:
        post_deploy_testing(token, voting_escrow, distributor)


def production():
    admin = get_admin()
    token_address = "0x10663b695b8f75647bd3ff0ff609e16d35bbd1ec"
    deploy_ve(admin, token_address, token_address)


def deploy_mock_erc20(admin):
    token = ERC20CRV.deploy("AmpliFi Test DAO Token", "testAGG", 18,
                            {"from": admin})
    return token


def deploy_ve(admin, token, reward_token_addr, start_time=1600300800, confs=1, deployments_json=None):
    voting_escrow = VotingEscrow.deploy(
        token,
        "Vote-escrowed AGG",
        "LAGG",
        "LAGG_1.0.0",
        EMERGENCY_ADMIN,
        {"from": admin},
    )
    # TODO : move to deploy_distributor function
    # start_time = 1600300800
    # distributor = FeeDistributor.deploy(
    #     voting_escrow.address,  # VotingEscrow
    #     start_time,
    #     reward_token_addr,
    #     OWNER_ADMIN,
    #     EMERGENCY_ADMIN,
    #     {"from": admin}
    # )
    deployments = {
        # "ERC20": token.address,
        # "VotingEscrow": voting_escrow.address,
        # "FeeDistributor": distributor.address
    }

    if deployments_json is not None:
        with open(deployments_json, "w") as fp:
            json.dump(deployments, fp)
        print(f"Deployment addresses saved to {deployments_json}")
    print("Deployed!")

    return token, voting_escrow  # , distributor


def post_deploy_testing(token, voting_escrow, distributor):
    amount = 2000 * 10 ** 18
    alice, bob = accounts[:2]
    token.approve(voting_escrow.address, amount, {"from": alice})
    print("approval amount", amount)
    old_alice_balance = voting_escrow.balanceOf(alice)
    assert voting_escrow.balanceOf(alice) == 0
    print("alice ve balance:", old_alice_balance)
    print("admin:", voting_escrow.admin())
    print("timestamp:", chain[-1].timestamp + MAXTIME)
    voting_escrow.create_lock(amount / 2, chain[-1].timestamp + MAXTIME, {"from": alice})
    print("alice ve", voting_escrow.balanceOf(alice))
    voting_escrow.create_lock_on_behalf(
        bob, amount / 2, chain[-1].timestamp + WEEK * 52, {"from": alice})
    print("bob ve balance", voting_escrow.balanceOf(bob))
    new_alice_balance = voting_escrow.balanceOf(alice)

    print("alice ve balance:", new_alice_balance)
    # test burn function
    # test burn with custom amount
    # test checkpoint


def get_admin():
    print("Deploying on chain id:", chain.id)
    if chain.id == 5 or chain.id == 421613:  # goerli eth or goerli arbitrum
        dev = accounts.load('100')
        network.priority_fee("4 gwei")
    elif chain.id == 42161:
        dev = accounts.load('100')

    else:
        dev = accounts[0]
    print("deploying with account:", dev)
    return dev
