# First time setup

```bash
git clone https://github.com/curvefi/curve-dao-contracts.git
cd curve-dao-contracts
pip install -r requirements.txt
npm i
pip install eth-brownie
brownie accounts new 100 # create a brownie account 100 and send some ETH to it to deploy
```

```bash
brownie networks add Ethereum arbitrum-goerli host=https://mainnet.infura.io/v3/7fb2e85974b5456cac23d39968f8eac1 chainid=421613
```

# Setup

```bash
brownie run scripts/deployment/deploy_dao development --network mainnet-fork
brownie run scripts/deployment/deploy_dao development --network goerli
```

# Other commands

```bash
brownie console --network mainnet-fork
```

# Testing

```bash
brownie test tests/unitary/VotingEscrow tests/unitary/FeeDistribution
brownie test tests/integration/VotingEscrow tests/integration/FeeDistributor
```
