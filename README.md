# 765_a3
1. Make sure you have the softwares in requirements.txt

2. Run the following command and copy the address to the genesis.json in the alloc section that adds the balance to the geth account.

geth --datadir $HOME/765_a3/test-eth1/ --password $HOME/765_a3/password.txt account new

3. Run the following command to set up the Ethereum node.

sh runEthereumNodeMy.sh

4. In a parallel terminal run the following.

bash run.sh
