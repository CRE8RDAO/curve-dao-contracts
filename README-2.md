# First time setup

```bash
git clone https://github.com/curvefi/curve-dao-contracts.git
cd curve-dao-contracts
pip install -r requirements.txt
npm i
pip install eth-brownie
brownie accounts new 100 # create a brownie account 100 and send some ETH to it to deploy
```

# Setup

```bash
brownie run scripts/deployment/deploy_dao development --network mainnet-fork
brownie run scripts/deployment/deploy_dao development --network goerli
```
