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
)

from . import deployment_config as config


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
    if len(accounts) == 0:  # if deploying to not locally
        print("accounts", accounts)
        dev = accounts.load('100')
    else:
        dev = accounts[0]
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
    # gauge_controller = GaugeController.deploy(
    #     token, voting_escrow, {"from": admin, "required_confs": confs}
    # )
    # for name, weight in GAUGE_TYPES:
    #     gauge_controller.add_type(name, weight, {"from": admin, "required_confs": confs})

    # pool_proxy = PoolProxy.deploy({"from": admin, "required_confs": confs})
    # minter = Minter.deploy(token, gauge_controller, {"from": admin, "required_confs": confs})
    # token.set_minter(minter, {"from": admin, "required_confs": confs})

    deployments = {
        "ERC20CRV": token.address,
        "VotingEscrow": voting_escrow.address,
    }
    # for name, (lp_token, weight) in POOL_TOKENS.items():
    #     gauge = LiquidityGauge.deploy(lp_token, minter, {"from": admin, "required_confs": confs})
    #     gauge_controller.add_gauge(gauge, 0, weight, {"from": admin, "required_confs": confs})
    #     deployments["LiquidityGauge"][name] = gauge.address

    # for (name, (lp_token, reward_claim, reward_token, weight)) in REWARD_POOL_TOKENS.items():
    #     gauge = LiquidityGaugeReward.deploy(
    #         lp_token, minter, reward_claim, reward_token, {"from": admin, "required_confs": confs}
    #     )
    #     gauge_controller.add_gauge(gauge, 0, weight, {"from": admin, "required_confs": confs})
    #     deployments["LiquidityGaugeReward"][name] = gauge.address

    print(f"Deployment complete! Total gas used: {sum(i.gas_used for i in history)}")
    if deployments_json is not None:
        with open(deployments_json, "w") as fp:
            json.dump(deployments, fp)
        print(f"Deployment addresses saved to {deployments_json}")
