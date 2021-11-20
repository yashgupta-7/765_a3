import sys
import time
import pprint

from web3 import Web3
from solcx import compile_source
import os

contract_source_path = os.environ['HOME']+'/765_a3/MyContract.sol'
logs = False
grcpt = False

def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()
   return compile_source(source)

def getReceipt(tx_hash3):
    '''Get and wait for receipts given a transaction hash'''
    while True:
        try: # keep trying until we get a  receipt
            time.sleep(0.1)
            receipt3 = w3.eth.getTransactionReceipt(tx_hash3)
            break
        except:
            continue
    receipt3 = w3.eth.getTransactionReceipt(tx_hash3)
    if receipt3 is not None and logs:
        print("empty:{0}".format(receipt3['gasUsed'])) #print amount of gas used for execution
    return

def registerUserTransaction(sort_contract, user_id, gr=False):
    '''Wrapper for calling registerUser function in solidity. Returns the hash of the tentative transaction.'''
    if logs:
        print("Registering User:", user_id)
    tx_hash = sort_contract.functions.registerUser(user_id, "YG").transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':2409638})
    if gr:
        getReceipt(tx_hash)
    return tx_hash

import numpy as np
def createAccTransaction(sort_contract, user_id_1, user_id_2, gr=False):
    '''Wrapper for calling createAcc function in solidity. Returns the hash of the tentative transaction.'''
    if logs:
        print("Creating Account between:", user_id_1, user_id_2)
    amt = int(np.random.exponential(10) * 0.5)
    tx_hash = sort_contract.functions.createAcc(user_id_1, user_id_2, amt).transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':2409638})
    if gr:
        getReceipt(tx_hash)
    return tx_hash

def closeAccTransaction(sort_contract, user_id_1, user_id_2, gr=False):
    '''Wrapper for calling closeAcc function in solidity. Returns the hash of the tentative transaction.'''
    if logs:
        print("Closing Account between:", user_id_1, user_id_2)
    tx_hash = sort_contract.functions.closeAcc(user_id_1, user_id_2).transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':2409638})
    if gr:
        getReceipt(tx_hash)
    return tx_hash

def sendAmountTransaction(sort_contract, user_id_1, user_id_2, amt, gr=False):
    '''Wrapper for calling sendAmount function in solidity. Returns the hash of the tentative transaction.'''
    if logs:
        print("Attempt to send ", amt, " from ", user_id_1, " to ", user_id_2)
    tx_hash = sort_contract.functions.sendAmount(user_id_1, user_id_2, amt).transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':2409638})
    if gr:
        getReceipt(tx_hash)
    return tx_hash

def getSucCountCall(sort_contract):
    '''Wrapper for checking succesful transaction count in solidity. Returns the number of succesful transactions.'''
    tx_hash = sort_contract.functions.getSucCount().call()
    print("Number of Successful Transactions:", tx_hash)
    return tx_hash

#######################################################################################################################
print("Starting Transaction Submission")
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:1558')) #start web3 on given port
w3.geth.miner.start(1) #start miner

with open(os.environ['HOME']+'/765_a3/MyContractAddressList') as fp:
    for line in fp:
        a,b = line.rstrip().split(':', 1)
        if a=="empty":
            contract_source_path = os.environ['HOME']+'/765_a3/MyContract.sol'
            compiled_sol = compile_source_file(contract_source_path) #compile solidity code
            contract_id, contract_interface = compiled_sol.popitem()
            sort_contract = w3.eth.contract(address=b, abi=contract_interface['abi']) #get contract

N = 100 #number of nodes
T = 1000 #number of transactions
interval = 100 #interval of logging and reporting
t = 0

# Register N users
wait_list = []
for i in range(N):
    wait_list.append(registerUserTransaction(sort_contract, i, gr=grcpt))
if not grcpt:
    for wl in wait_list:
        getReceipt(wl)

#Construct power law degree distribution graph using networkx
import networkx
power_graph = networkx.barabasi_albert_graph(N, int(0.7*N))

#create accounts according to transactions
wait_list = []
# for i in range(N):
#     for j in range(i, N):
#         edge = (i, j)
for edge in power_graph.edges:
        # print(edge)
        wait_list.append(createAccTransaction(sort_contract, edge[0], edge[1], gr=grcpt))
if not grcpt:
    for wl in wait_list:
        getReceipt(wl)

#get initial succesful transaction count. should be 0.
getSucCountCall(sort_contract)

wait_list = []
while (t<T):
    sender = np.random.randint(N)
    recvr = np.random.randint(N)
    if (sender==recvr): #if sender and reciever same continue
        continue
    t += 1
    wait_list.append(sendAmountTransaction(sort_contract, sender, recvr, 1, gr=grcpt)) #send amount transaction between sender and reciever
    if (t%interval==0):
        if not grcpt:
            for wl in wait_list:
                getReceipt(wl)
        wait_list = []
        getSucCountCall(sort_contract)
        print("Number of Total Transactions:", t)

w3.geth.miner.stop() #stop miner