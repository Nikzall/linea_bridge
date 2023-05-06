from web3 import Web3
from eth_account.account import Account
import time
from eth_utils import function_signature_to_4byte_selector
from eth_abi import encode
from time import ctime
import csv
from config import *
import random

node = RPC['goerli']
node_bnb = RPC['bnb_testnet']
gasPriceLimit = Web3.to_wei(GAS_PRICE_LIMIT, 'gwei')

w3 = Web3(Web3.HTTPProvider(node))
w3_bnb = Web3(Web3.HTTPProvider(node_bnb))

#---------------------------------------bnb transactions
def bnb_bridge(account, name):
    print(f"[{ctime(time.time())}]:starting bnb brdidge with wallet {name}")
    chaindId = 59140
    mintAccount = account.address
    amount = w3_bnb.toWei(0.01, "ether")
    nonce = int(time.time())
    function_name = "depositNative"
    params_type = "uint256", "uint64",  "address", "uint64"
    function_selector = function_signature_to_4byte_selector(f"{function_name}({','.join(params_type)})")
    function_params = amount, chaindId, mintAccount, nonce
    encoded_params = encode(params_type, function_params)
    transaction_data = "0x" + function_selector.hex() + encoded_params.hex()
    tx = {
        "from": account.address,
        "to": w3_bnb.toChecksumAddress("0x62d06e1e3c6C202B60BE4c0E03ea8d6fcA88165f"),
        "gasPrice": int(w3_bnb.eth.gas_price*1.2),
        "nonce": w3_bnb.eth.get_transaction_count(account.address),
        "data": transaction_data,
        "value": w3_bnb.toWei(0.01, "ether")
    }
    try:
        tx['gas'] = w3_bnb.eth.estimate_gas(tx)
        signed_tx = account.sign_transaction(tx)
        signed_transfer_hash = w3_bnb.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"[{ctime(time.time())}]:sent bnb bridge transaction with hash {signed_transfer_hash.hex()}, from wallet {name}")
    except Exception as e:
        print(f"[{ctime(time.time())}]:error {e} while estimating gas for {name} during bnb bridge")
    time.sleep(random.uniform(NEXT_TX_MIN_WAIT_TIME,NEXT_TX_MAX_WAIT_TIME))

def busd_approve(account, name):
    print(f"[{ctime(time.time())}]:starting busd approve with wallet {name}")
    tx = {
        "from": account.address,
        "to": w3_bnb.toChecksumAddress("0xeb3eb991d39dac92616da64b7c6d5af5ccff1627"),
        "gasPrice": int(w3_bnb.eth.gas_price*1.2),
        "nonce": w3_bnb.eth.get_transaction_count(account.address),
        "data": "0x095ea7b300000000000000000000000062d06e1e3c6c202b60be4c0e03ea8d6fca88165fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    }
    try:
        tx['gas'] = w3_bnb.eth.estimate_gas(tx)
        signed_tx = account.sign_transaction(tx)
        signed_transfer_hash = w3_bnb.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"[{ctime(time.time())}]:sent busd approve with hash {signed_transfer_hash.hex()}, from wallet {name}")
    except Exception as e:
        print(f"[{ctime(time.time())}]:error {e} while estimating gas for {name} during busd approve")
    time.sleep(random.uniform(NEXT_TX_MIN_WAIT_TIME,NEXT_TX_MAX_WAIT_TIME))

def busd_bridge(account, name):
    print(f"[{ctime(time.time())}]:starting bnb brdidge with wallet {name}")
    token_address = "0xeB3Eb991D39Dac92616da64b7c6D5af5cCFf1627",
    amount = 100000000000000000000
    chaindId = 59140
    mintAccount = account.address
    amount = w3_bnb.toWei(0.01, "ether")
    nonce = int(time.time())
    function_name = "deposit"
    params_type = "address", "uint256", "uint64",  "address", "uint64"
    function_selector = function_signature_to_4byte_selector(f"{function_name}({','.join(params_type)})")
    function_params = token_address, amount, chaindId, mintAccount, nonce
    encoded_params = encode(params_type, function_params)
    transaction_data = "0x" + function_selector.hex() + encoded_params.hex()
    tx = {
        "from": account.address,
        "to": w3_bnb.toChecksumAddress("0x62d06e1e3c6C202B60BE4c0E03ea8d6fcA88165f"),
        "gasPrice": int(w3_bnb.eth.gas_price*1.2),
        "nonce": w3_bnb.eth.get_transaction_count(account.address),
        "data": transaction_data,
        "value": 0
    }
    try:
        tx['gas'] = w3_bnb.eth.estimate_gas(tx)
        signed_tx = account.sign_transaction(tx)
        signed_transfer_hash = w3_bnb.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"[{ctime(time.time())}]:sent bnb bridge transaction with hash {signed_transfer_hash.hex()}, from wallet {name}")
    except Exception as e:
        print(f"[{ctime(time.time())}]:error {e} while estimating gas for {name} during bnb bridge")
    time.sleep(random.uniform(NEXT_TX_MIN_WAIT_TIME,NEXT_TX_MAX_WAIT_TIME))
#-------------------------------------------------------

#---------------------------------------goerli transactions
def dai_mint(account, name):
    while True:
        if w3.eth.gas_price<gasPriceLimit:
            print(f"[{ctime(time.time())}]:starting dai mint with wallet {name}")
            address = account.address[2:]
            tx = {
                "from": account.address,
                "to": w3.toChecksumAddress("0xb93cba7013f4557cdfb590fd152d24ef4063485f"),
                "value": w3.toWei(0.01, "ether"),
                "gasPrice": int(w3.eth.gas_price*1.2),
                "nonce": w3.eth.get_transaction_count(account.address),
                "data": f"0x40c10f19000000000000000000000000{address}000000000000000000000000000000000000000000000001158e460913d00000"
            }
            try:
                tx['gas'] = w3.eth.estimate_gas(tx)
                signed_tx = account.sign_transaction(tx)
                signed_transfer_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
                print(f"[{ctime(time.time())}]:sent dai mint transaction with hash {signed_transfer_hash.hex()}, from wallet {name}")
            except Exception as e:
                print(f"[{ctime(time.time())}]:error {e} while estimating gas for {name} during dai mint")
            time.sleep(random.uniform(NEXT_TX_MIN_WAIT_TIME,NEXT_TX_MAX_WAIT_TIME))
            break
        else:
            time.sleep(random.uniform(NEXT_TX_MIN_WAIT_TIME,NEXT_TX_MAX_WAIT_TIME))
    
def dai_approve(account, name):
    while True:
        if w3.eth.gas_price<gasPriceLimit:
            print(f"[{ctime(time.time())}]:starting dai approve with wallet {name}")
            tx = {
                "from": account.address,
                "to": w3.toChecksumAddress("0xb93cba7013f4557cDFB590fD152d24Ef4063485f"),
                "gasPrice": int(w3.eth.gas_price*1.2),
                "nonce": w3.eth.get_transaction_count(account.address),
                "data": "0x095ea7b3000000000000000000000000aa1603822b43e592e33b58d34b4423e1bcd8b4dcffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
            }
            try:
                tx['gas'] = w3.eth.estimate_gas(tx)
                signed_tx = account.sign_transaction(tx)
                signed_transfer_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
                print(f"[{ctime(time.time())}]:sent dai approve with hash {signed_transfer_hash.hex()}, from wallet {name}")
            except Exception as e:
                print(f"[{ctime(time.time())}]:error {e} while estimating gas for {name} during dai approve")
            time.sleep(random.uniform(NEXT_TX_MIN_WAIT_TIME,NEXT_TX_MAX_WAIT_TIME))
            break
        else:
            time.sleep(random.uniform(NEXT_TX_MIN_WAIT_TIME,NEXT_TX_MAX_WAIT_TIME))

def dai_bridge(account, name):
    while True:
        if w3.eth.gas_price<gasPriceLimit:
            print(f"[{ctime(time.time())}]:starting dai brdidge with wallet {name}")
            chaind_id = 59140
            reciepent = account.address
            amount = w3.toWei(10, "ether")
            amount_out = 0
            deadline = int(time.time())+7*24*60*60
            relayer = "0xB47dE784aB8702eC35c5eAb225D6f6cE476DdD28"
            relayerFee = 0
            function_name = "sendToL2"
            params_type = "uint256", "address", "uint256", "uint256", "uint256", "address", "uint256"
            function_selector = function_signature_to_4byte_selector(f"{function_name}({','.join(params_type)})")
            function_params = chaind_id, reciepent, amount, amount_out, deadline, relayer, relayerFee
            encoded_params = encode(params_type, function_params)
            transaction_data = "0x" + function_selector.hex() + encoded_params.hex()
            tx = {
                "from": account.address,
                "to": w3.toChecksumAddress("0xb93cba7013f4557cDFB590fD152d24Ef4063485f"),
                "gasPrice": int(w3.eth.gas_price*1.2),
                "nonce": w3.eth.get_transaction_count(account.address),
                "data": transaction_data,
                "value": w3.toWei(0.01, "ether")
            }
            try:
                w3.eth.estimate_gas(tx)
                tx['gas'] = GAS_LIMIT_FOR_GOERLI_BRIDGE
                signed_tx = account.sign_transaction(tx)
                signed_transfer_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
                print(f"[{ctime(time.time())}]:sent dai bridge transaction with hash {signed_transfer_hash.hex()}, from wallet {name}")
            except Exception as e:
                print(f"[{ctime(time.time())}]:error {e} while estimating gas for {name} during dai bridge")
            time.sleep(random.uniform(NEXT_TX_MIN_WAIT_TIME,NEXT_TX_MAX_WAIT_TIME))
            break
        else:
            time.sleep(random.uniform(NEXT_TX_MIN_WAIT_TIME,NEXT_TX_MAX_WAIT_TIME))

def hop_mint(account, name):
    while True:
        if w3.eth.gas_price<gasPriceLimit:
            print(f"[{ctime(time.time())}]:starting hop mint with wallet {name}")
            address = account.address[2:]
            tx = {
                "from": account.address,
                "to": w3.toChecksumAddress("0x38af6928bf1fd6b3c768752e716c49eb8206e20c"),
                "value": w3.toWei(0.1, "ether"),
                "gasPrice": int(w3.eth.gas_price*1.2),
                "nonce": w3.eth.get_transaction_count(account.address),
                "data": f"0x40c10f19000000000000000000000000{address}00000000000000000000000000000000000000000000003635c9adc5dea00000"
            }
            try:
                tx['gas'] = w3.eth.estimate_gas(tx)
                signed_tx = account.sign_transaction(tx)
                signed_transfer_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
                print(f"[{ctime(time.time())}]:sent hop mint with hash {signed_transfer_hash.hex()}, from wallet {name}")
            except Exception as e:
                print(f"[{ctime(time.time())}]:error {e} while estimating gas for {name} during hop mint")
            time.sleep(random.uniform(NEXT_TX_MIN_WAIT_TIME,NEXT_TX_MAX_WAIT_TIME))
            break
        else:
            time.sleep(random.uniform(NEXT_TX_MIN_WAIT_TIME,NEXT_TX_MAX_WAIT_TIME))

def hop_approve(account, name):
    while True:
        if w3.eth.gas_price<gasPriceLimit:
            print(f"[{ctime(time.time())}]:starting hop approve with wallet {name}")
            tx = {
                "from": account.address,
                "to": w3.toChecksumAddress("0x38af6928bf1fd6b3c768752e716c49eb8206e20c"),
                "gasPrice": int(w3.eth.gas_price*1.2),
                "nonce": w3.eth.get_transaction_count(account.address),
                "data": "0x095ea7b3000000000000000000000000aa1603822b43e592e33b58d34b4423e1bcd8b4dcffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
            }
            try:
                tx['gas'] = w3.eth.estimate_gas(tx)
                signed_tx = account.sign_transaction(tx)
                signed_transfer_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
                print(f"[{ctime(time.time())}]:sent hop approve with hash {signed_transfer_hash.hex()}, from wallet {name}")
            except Exception as e:
                print(f"[{ctime(time.time())}]:error {e} while estimating gas for {name} during hop approve")
            time.sleep(random.uniform(NEXT_TX_MIN_WAIT_TIME,NEXT_TX_MAX_WAIT_TIME))
            break
        else:
            time.sleep(random.uniform(NEXT_TX_MIN_WAIT_TIME,NEXT_TX_MAX_WAIT_TIME))

def hop_bridge(account, name):
    while True:
        if w3.eth.gas_price<gasPriceLimit:
            print(f"[{ctime(time.time())}]:starting hop bridge with wallet {name}")
            chaind_id = 59140
            reciepent = account.address
            amount = w3.toWei(120, "ether")
            amount_out = 0
            deadline = int(time.time())+7*24*60*60
            relayer = "0xB47dE784aB8702eC35c5eAb225D6f6cE476DdD28"
            relayerFee = 0
            function_name = "sendToL2"
            params_type = "uint256", "address", "uint256", "uint256", "uint256", "address", "uint256"
            function_selector = function_signature_to_4byte_selector(f"{function_name}({','.join(params_type)})")
            function_params = chaind_id, reciepent, amount, amount_out, deadline, relayer, relayerFee
            encoded_params = encode(params_type, function_params)
            transaction_data = "0x" + function_selector.hex() + encoded_params.hex()
            tx = {
                "from": account.address,
                "to": w3.toChecksumAddress("0x9051dc48d27dab53dbab9e844f8e48c469603938"),
                "gasPrice": int(w3.eth.gas_price*1.2),
                "nonce": w3.eth.get_transaction_count(account.address),
                "data": transaction_data,
                "value": w3.toWei(0.01, "ether")
            }
            try:
                w3.eth.estimate_gas(tx)
                tx['gas'] = GAS_LIMIT_FOR_GOERLI_BRIDGE
                signed_tx = account.sign_transaction(tx)
                signed_transfer_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
                print(f"[{ctime(time.time())}]:sent hop bridge transaction with hash {signed_transfer_hash.hex()}, from wallet {name}")
            except Exception as e:
                print(f"[{ctime(time.time())}]:error {e} while estimating gas for {name} during hop bridge")
            time.sleep(random.uniform(NEXT_TX_MIN_WAIT_TIME,NEXT_TX_MAX_WAIT_TIME))
            break
        else:
            time.sleep(random.uniform(NEXT_TX_MIN_WAIT_TIME,NEXT_TX_MAX_WAIT_TIME))

def geth_bridge(account, name):
    while True:
        if w3.eth.gas_price<gasPriceLimit:
            print(f"[{ctime(time.time())}]:starting geth bridge with wallet {name}")
            chaind_id = 59140
            reciepent = account.address
            amount = w3.toWei(0.1, "ether")
            amount_out = 0
            deadline = int(time.time())+7*24*60*60
            relayer = "0xB47dE784aB8702eC35c5eAb225D6f6cE476DdD28"
            relayerFee = 10000000000000000
            function_name = "sendToL2"
            params_type = "uint256", "address", "uint256", "uint256", "uint256", "address", "uint256"
            function_selector = function_signature_to_4byte_selector(f"{function_name}({','.join(params_type)})")
            function_params = chaind_id, reciepent, amount, amount_out, deadline, relayer, relayerFee
            encoded_params = encode(params_type, function_params)
            transaction_data = "0x" + function_selector.hex() + encoded_params.hex()
            tx = {
                "from": account.address,
                "to": w3.toChecksumAddress("0x9051dc48d27dab53dbab9e844f8e48c469603938"),
                "gasPrice": int(w3.eth.gas_price*1.2),
                "nonce": w3.eth.get_transaction_count(account.address),
                "data": transaction_data,
                "value": w3.toWei(0.11, "ether")
            }
            try:
                w3.eth.estimate_gas(tx)
                tx['gas'] = GAS_LIMIT_FOR_GOERLI_BRIDGE
                signed_tx = account.sign_transaction(tx)
                signed_transfer_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
                print(f"[{ctime(time.time())}]:sent geth bridge transaction with hash {signed_transfer_hash.hex()}, from wallet {name}")
            except Exception as e:
                print(f"[{ctime(time.time())}]:error {e} while estimating gas for {name} during geth bridge")
            time.sleep(random.uniform(NEXT_TX_MIN_WAIT_TIME,NEXT_TX_MAX_WAIT_TIME))
            break
        else:
            time.sleep(random.uniform(NEXT_TX_MIN_WAIT_TIME,NEXT_TX_MAX_WAIT_TIME))

def bridge_to_bnb(account, name):
    while True:
        address = account.address[2:]
        if w3.eth.gas_price<gasPriceLimit:
            print(f"[{ctime(time.time())}]:starting geth to bnb bridge with wallet {name}")
            tx = {
                "chainId": 5,
                "from": account.address,
                "to": w3.toChecksumAddress("0x7c125C1d515b8945841b3d5144a060115C58725F"),
                "gasPrice": int(w3.eth.gas_price*1.2),
                "nonce": w3.eth.get_transaction_count(account.address),
                "value": w3.to_wei(0.1, 'ether'),
                "data": f"0x71ec5c05aa669c4922569c1d33f7a81aaa21813800000000000000000000000013a0c5930c028511dc02665e7285134b6d11a5f4000000000000000000000000{address}0000000000000000000000000000000000000000000000000000000000000000"
            }
            try:
                w3.eth.estimate_gas(tx)
                tx['gas'] = GAS_LIMIT_FOR_GOERLI_BRIDGE
                signed_tx = account.sign_transaction(tx)
                signed_transfer_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
                print(f"[{ctime(time.time())}]:sent geth to bnb bridge with hash {signed_transfer_hash.hex()}, from wallet {name}")
            except Exception as e:
                print(f"[{ctime(time.time())}]:error {e} while estimating gas for {name} during geth to bnb bridge")
            time.sleep(random.uniform(NEXT_TX_MIN_WAIT_TIME,NEXT_TX_MAX_WAIT_TIME))
            break
        else:
            sleep_time = random.uniform(NEXT_TX_MIN_WAIT_TIME,NEXT_TX_MAX_WAIT_TIME)
            print(f"gas to gigh waiting for {sleep_time}")
            time.sleep(sleep_time)

#-------------------------------------------------------------

account_list = []

with open("wallets.csv") as file:
    reader = csv.DictReader(file)
    content =[row for row in reader]
    for row in content:
            row['key'] = Account.from_key(row['key'])
            account_list.append({'name': row['name'], 'account': row['key']})

print(f"[{ctime(time.time())}]:starting tasks with {len(account_list)} wallets")



for account in account_list:
    bridge_to_bnb(account['account'], account['name'])
    time_sleep = random.uniform(NEXT_ADDRESS_MIN_WAIT_TIME*60,NEXT_ADDRESS_MAX_WAIT_TIME*60)
    print(f"sleeping for {time_sleep}")
    time.sleep(time_sleep)

print("script finished")
