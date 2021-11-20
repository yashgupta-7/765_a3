import sys
import time
import pprint

import web3
from web3 import Web3
from solcx import compile_source
import os

def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()
   return compile_source(source)

def read_address_file(file_path):
    file = open(file_path, 'r')
    addresses = file.read().splitlines() 
    return addresses


def connectWeb3():
    # print(os.environ['HOME']+'/HW3/test-eth1/geth.ipc')
    # return web3.Web3(HTTPProvider(os.environ['HOME']+'/HW3/test-eth1/geth.ipc', timeout=100000))
    return Web3(Web3.HTTPProvider('http://127.0.0.1:1558'))
    


def deployEmptyContract(contract_source_path, w3, account):
    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface3 = compiled_sol.popitem()
    # print(contract_id, contract_interface3)
    curBlock = w3.eth.getBlock('latest')
    tx_hash = w3.eth.contract(
            abi=contract_interface3['abi'],
            bytecode=contract_interface3['bin']).constructor().transact({'txType':"0x0", 'from':account, 'gas':1000000})
    return tx_hash

def deployContracts(w3, account):
    tx_hash3 = deployEmptyContract(empty_source_path, w3, account)

    while True:
        try:
            receipt3 = w3.eth.getTransactionReceipt(tx_hash3)
            break
        except:
            time.sleep(1)
            continue
    # while ((receipt3 is None)) :
    #     time.sleep(1)
    #     receipt3 = w3.eth.getTransactionReceipt(tx_hash3)

    w3.geth.miner.stop()

    if receipt3 is not None:
        print("empty:{0}".format(receipt3['contractAddress']))


empty_source_path = os.environ['HOME']+'/765_a3/MyContract.sol'


w3 = connectWeb3()
# print(w3, w3.isConnected())
w3.geth.miner.start(1)
time.sleep(4)
# print(w3.eth.accounts)
deployContracts(w3, w3.eth.accounts[0])