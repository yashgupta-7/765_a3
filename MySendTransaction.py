import sys
import time
import pprint

from web3 import Web3
from solcx import compile_source
import os

contract_source_path = os.environ['HOME']+'/765_a3/MyContract.sol'
logs = True
grcpt = False

def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()
   return compile_source(source)

def getReceipt(tx_hash3):
    # receipt3 = w3.eth.getTransactionReceipt(tx_hash3)
    while True:
        try: 
            time.sleep(0.1)
            receipt3 = w3.eth.getTransactionReceipt(tx_hash3)
            break
        except:
            continue
    receipt3 = w3.eth.getTransactionReceipt(tx_hash3)
    if receipt3 is not None and logs:
        print("empty:{0}".format(receipt3['gasUsed']))
    return

def registerUserTransaction(sort_contract, user_id, gr=False):
    if logs:
        print("Registering User:", user_id)
    tx_hash = sort_contract.functions.registerUser(user_id, "YG").transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':2409638})
    if gr:
        getReceipt(tx_hash)
    return tx_hash

import numpy as np
def createAccTransaction(sort_contract, user_id_1, user_id_2, gr=False):
    if logs:
        print("Creating Account between:", user_id_1, user_id_2)
    amt = int(np.random.exponential(10) * 0.5)
    tx_hash = sort_contract.functions.createAcc(user_id_1, user_id_2, amt).transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':2409638})
    if gr:
        getReceipt(tx_hash)
    return tx_hash

def closeAccTransaction(sort_contract, user_id_1, user_id_2, gr=False):
    if logs:
        print("Closing Account between:", user_id_1, user_id_2)
    tx_hash = sort_contract.functions.closeAcc(user_id_1, user_id_2).transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':2409638})
    if gr:
        getReceipt(tx_hash)
    return tx_hash

def sendAmountTransaction(sort_contract, user_id_1, user_id_2, amt, gr=False):
    if logs:
        print("Attempt to send ", amt, " from ", user_id_1, " to ", user_id_2)
    tx_hash = sort_contract.functions.sendAmount(user_id_1, user_id_2, amt).transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':2409638})
    if gr:
        getReceipt(tx_hash)
    return tx_hash

def getSucCountCall(sort_contract):
    tx_hash = sort_contract.functions.getSucCount().call()
    print("Number of Successful Transactions:", tx_hash)
    return tx_hash

def sendEmptyLoopTransaction(address):   
    contract_source_path = os.environ['HOME']+'/HW3/emptyLoop.sol'
    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface = compiled_sol.popitem()
    sort_contract = w3.eth.contract(
    address=address,
    abi=contract_interface['abi'])
    tx_hash = sort_contract.functions.runLoop().transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':2409638})
    print(tx_hash)
    return tx_hash

#######################################################################################################################
print("Starting Transaction Submission")
# w3 = Web3(IPCProvider(os.environ['HOME']+'/HW3/test-eth1/geth.ipc', timeout=100000))
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:1558'))
w3.geth.miner.start(1)

with open(os.environ['HOME']+'/765_a3/MyContractAddressList') as fp:
    for line in fp:
        #print(line)
        a,b = line.rstrip().split(':', 1)
        if a=="empty":
            contract_source_path = os.environ['HOME']+'/765_a3/MyContract.sol'
            compiled_sol = compile_source_file(contract_source_path)
            contract_id, contract_interface = compiled_sol.popitem()
            sort_contract = w3.eth.contract(address=b, abi=contract_interface['abi'])
            # tx_hash3 = sendEmptyLoopTransaction(b) 
        time.sleep(0.01)

# time.sleep(50)
N = 10
T = 1000
interval = 100
t = 0

wait_list = []
for i in range(N):
    wait_list.append(registerUserTransaction(sort_contract, i, gr=grcpt))
if not grcpt:
    for wl in wait_list:
        getReceipt(wl)

import networkx
power_graph = networkx.barabasi_albert_graph(N, 7)

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

getSucCountCall(sort_contract)

wait_list = []
while (t<T):
    sender = np.random.randint(N)
    recvr = np.random.randint(N)
    if (sender==recvr):
        continue
    t += 1
    wait_list.append(sendAmountTransaction(sort_contract, sender, recvr, 1, gr=grcpt))
    if (t%interval==0):
        if not grcpt:
            for wl in wait_list:
                getReceipt(wl)
        wait_list = []
        getSucCountCall(sort_contract)
        print("Number of Total Transactions:", t)

w3.geth.miner.stop()