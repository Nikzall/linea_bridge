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
gasPriceLimit = GAS_PRICE_LIMIT

w3 = Web3(Web3.HTTPProvider(node))

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
                print(f"[{ctime(time.time())}]:sent dai mint transaction with hash {signed_transfer_hash}, from wallet {name}")
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
                print(f"[{ctime(time.time())}]:sent dai approve with hash {signed_transfer_hash}, from wallet {name}")
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
                print(f"[{ctime(time.time())}]:sent dai bridge transaction with hash {signed_transfer_hash}, from wallet {name}")
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
                print(f"[{ctime(time.time())}]:sent hop mint with hash {signed_transfer_hash}, from wallet {name}")
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
                print(f"[{ctime(time.time())}]:sent hop approve with hash {signed_transfer_hash}, from wallet {name}")
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
                print(f"[{ctime(time.time())}]:sent hop bridge transaction with hash {signed_transfer_hash}, from wallet {name}")
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
                print(f"[{ctime(time.time())}]:sent geth bridge transaction with hash {signed_transfer_hash}, from wallet {name}")
            except Exception as e:
                print(f"[{ctime(time.time())}]:error {e} while estimating gas for {name} during geth bridge")
            time.sleep(random.uniform(NEXT_TX_MIN_WAIT_TIME,NEXT_TX_MAX_WAIT_TIME))
            break
        else:
            time.sleep(random.uniform(NEXT_TX_MIN_WAIT_TIME,NEXT_TX_MAX_WAIT_TIME))

account_list = []

with open("wallets.csv") as file:
    reader = csv.DictReader(file)
    content =[row for row in reader]
    for row in content:
            row['key'] = Account.from_key(row['key'])
            account_list.append({'name': row['name'], 'account': row['key']})

print(f"[{ctime(time.time())}]:starting tasks with {len(account_list)} wallets")



for account in account_list:
    dai_mint(account['account'], account['name'])
    dai_approve(account['account'], account['name'])
    dai_bridge(account['account'], account['name'])
    hop_mint(account['account'], account['name'])
    hop_approve(account['account'], account['name'])
    hop_bridge(account['account'], account['name'])
    time.sleep(random.uniform(NEXT_ADDRESS_MIN_WAIT_TIME*60,NEXT_ADDRESS_MAX_WAIT_TIME*60))
