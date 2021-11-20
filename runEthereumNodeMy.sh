# !/bin/bash
rm -r test-eth1/geth/chaindata/;
rm -r test-eth1/geth/lightchaindata/;
rm -r test-eth1/geth/nodes/;
rm -r test-eth1/geth/ethash/;
rm test-eth1/geth/LOCK;
rm test-eth1/geth/transactions.rlp;
# $HOME/go-ethereum/build/bin/geth --datadir $HOME/HW3/test-eth1 --rpc --rpcport=1558 --rpcapi "eth,net,web3,debug" --networkid=2310 --port=1547 --hashpower 70 --interarrival 5 --syncmode full --gcmode archive --nodiscover --nodekey=nk.txt init $HOME/HW3/genesis.json
geth --datadir test-eth1 --http --http.port=1558 --http.api "eth,net,web3,debug,miner" --networkid=2310 --port=1547  --syncmode full --gcmode archive --nodiscover --nodekey=nk.txt init genesis.json
gnome-terminal --geometry 90x25+1300+1550 -- bash startIpc.sh 1
# $HOME/go-ethereum/build/bin/geth --datadir $HOME/HW3/test-eth1 --rpc --rpcport=1558 --rpcapi "eth,net,web3,debug" --networkid=2310 --port=1547 --hashpower 70 --interarrival 5 --syncmode full --gcmode archive --nodiscover --nodekey=nk.txt --verbosity 5 --allow-insecure-unlock --unlock 0 --password password.txt
geth --datadir test-eth1 --http --http.port=1558 --http.api  "eth,net,web3,debug,miner" --networkid=2310 --port=1547 --syncmode full --gcmode archive --nodiscover --nodekey=nk.txt --verbosity 5 --allow-insecure-unlock --unlock 0 --password password.txt