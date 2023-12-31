import os
import logging
import time
from web3 import Web3
from compiled_contracts.goerli_wsibr_v9 import compiled_goerli_wsibr_v9
from compiled_contracts.goerli_msw_issue_v6 import compiled_goerli_msw_issue_v6

from compiled_contracts.sibr_msw_issue_v6 import compiled_sibr_msw_issue_v6
from compiled_contracts.sibr_weth_v9 import compiled_sibr_weth_v9

logging.basicConfig(level=logging.DEBUG)
#IS_INFURA = True
infura_url = 'https://goerli.infura.io/v3/8596c2e3a7704213911e675a8eedd635'
#infura_url = 'https://rpc.test.siberium.net'
first_adr = '0xade657554299E886Fb0150d4293D441f278A9854'
second_adr = "0xc6322A3D73f791dFf977984F5380468885Beed77"
third_adr = "0xe52FB548417eE451192200fdAf8Fa1511daB2300"
fourth_adr = '0xCdf38647E1333C50Ec2F1104A25F88D16094D327'
first_adr_pk = '62827a79fb937313b7d736e973f4ca8a33581650f153107de18114ef84a30347'
second_adr_pk = '540884f10d684620077d6b90a65c1a256f3f00172df5635d73c99178c45950af'
third_adr_pk = 'c0fcfbef21969b71702481d5023e5ef1cf07ad4a3f0da7d2d71cfdea0e0c7abc'
fourth_adr_pk = 'a83c718255dc6fe17fa90304ee4bea9fa9d7a74d1eb402d69481b009bd8507bc'
adrs_pk = {
    first_adr: first_adr_pk,
    second_adr: second_adr_pk,
    third_adr: third_adr_pk,
    fourth_adr: fourth_adr_pk
}
#goerli_ms_sc_adr_test = '0x0466B5ccccE6c334331f3fB08a5ff26c29B5E7eA'
#goerli_ms_sc_abi = '[{"inputs":[{"internalType":"address[]","name":"_owners","type":"address[]"},{"internalType":"uint256","name":"_numConfirmationsRequired","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"uint256","name":"txIndex","type":"uint256"}],"name":"ConfirmTransaction","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"balance","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"uint256","name":"txIndex","type":"uint256"}],"name":"ExecuteTransaction","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"uint256","name":"issueIndex","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"IssueInited","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"uint256","name":"issueIndex","type":"uint256"}],"name":"IssueProvided","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"uint256","name":"issueIndex","type":"uint256"}],"name":"IssueSigned","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"uint256","name":"txIndex","type":"uint256"}],"name":"RevokeConfirmation","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"uint256","name":"txIndex","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"},{"indexed":false,"internalType":"bytes","name":"data","type":"bytes"}],"name":"SubmitTransaction","type":"event"},{"inputs":[],"name":"WETHSTokenAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_txIndex","type":"uint256"}],"name":"confirmTransaction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_txIndex","type":"uint256"}],"name":"executeTransaction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_issueIndex","type":"uint256"}],"name":"getIssue","outputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bool","name":"provided","type":"bool"},{"internalType":"uint256","name":"numSigns","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getIssuesCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getOwners","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_txIndex","type":"uint256"}],"name":"getTransaction","outputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"bool","name":"executed","type":"bool"},{"internalType":"uint256","name":"numConfirmations","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTransactionCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"initIssue","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"name":"isConfirmed","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"isOwner","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"name":"isSigned","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"issues","outputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bool","name":"provided","type":"bool"},{"internalType":"uint256","name":"numSigns","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"numConfirmationsRequired","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"numSignsRequired","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"owners","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_issueIndex","type":"uint256"}],"name":"provideIssue","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_txIndex","type":"uint256"}],"name":"revokeConfirmation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_issueIndex","type":"uint256"}],"name":"signIssue","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"submitTransaction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"transactions","outputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"bool","name":"executed","type":"bool"},{"internalType":"uint256","name":"numConfirmations","type":"uint256"}],"stateMutability":"view","type":"function"},{"stateMutability":"payable","type":"receive"}]'

#sibr_ms_sc_adr_test = "0x14DE0EAe16cFd97Eb19e4a97d82Dad72E02D6A8A"
#sibr_ms_sc_abi = '[{"inputs":[{"internalType":"address[]","name":"_owners","type":"address[]"},{"internalType":"uint256","name":"_numConfirmationsRequired","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"uint256","name":"txIndex","type":"uint256"}],"name":"ConfirmTransaction","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"balance","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"uint256","name":"txIndex","type":"uint256"}],"name":"ExecuteTransaction","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"uint256","name":"issueIndex","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"IssueInited","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"uint256","name":"issueIndex","type":"uint256"}],"name":"IssueProvided","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"uint256","name":"issueIndex","type":"uint256"}],"name":"IssueSigned","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"uint256","name":"txIndex","type":"uint256"}],"name":"RevokeConfirmation","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"uint256","name":"txIndex","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"},{"indexed":false,"internalType":"bytes","name":"data","type":"bytes"}],"name":"SubmitTransaction","type":"event"},{"inputs":[],"name":"WETHSTokenAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_txIndex","type":"uint256"}],"name":"confirmTransaction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_txIndex","type":"uint256"}],"name":"executeTransaction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_issueIndex","type":"uint256"}],"name":"getIssue","outputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bool","name":"provided","type":"bool"},{"internalType":"uint256","name":"numSigns","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getIssuesCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getOwners","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_txIndex","type":"uint256"}],"name":"getTransaction","outputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"bool","name":"executed","type":"bool"},{"internalType":"uint256","name":"numConfirmations","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTransactionCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"initIssue","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"name":"isConfirmed","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"isOwner","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"name":"isSigned","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"issues","outputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bool","name":"provided","type":"bool"},{"internalType":"uint256","name":"numSigns","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"numConfirmationsRequired","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"numSignsRequired","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"owners","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_issueIndex","type":"uint256"}],"name":"provideIssue","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_txIndex","type":"uint256"}],"name":"revokeConfirmation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_issueIndex","type":"uint256"}],"name":"signIssue","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"submitTransaction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"transactions","outputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"bool","name":"executed","type":"bool"},{"internalType":"uint256","name":"numConfirmations","type":"uint256"}],"stateMutability":"view","type":"function"},{"stateMutability":"payable","type":"receive"}]'


def standard_trx_build_for_usual_trans(base_adr=None) -> dict:
    if base_adr is None:
        base_adr = first_adr
    web3 = Web3(Web3.HTTPProvider(infura_url, request_kwargs={'timeout': 60}))

    base_fee = web3.eth.get_block('latest').baseFeePerGas
    priority_fee = web3.eth.max_priority_fee
    max_fee = priority_fee + base_fee  #  + 2 * base_fee

    build_trx_config = {
        'chainId': web3.eth.chain_id,
        'from': base_adr,
        'nonce': web3.eth.get_transaction_count(base_adr),
        # 'gasPrice': web3.eth.gas_price,
        'maxFeePerGas': max_fee,  # 30000000000,
        'maxPriorityFeePerGas': priority_fee  # 3000000000,
    }
    build_trx_config['gas'] = web3.eth.estimate_gas(build_trx_config)

    return build_trx_config


def standard_trx_build_for_sc_call_with_gas(base_adr=None) -> dict:
    if base_adr is None:
        base_adr = first_adr
    web3 = Web3(Web3.HTTPProvider(infura_url, request_kwargs={'timeout': 60}))

    base_fee = web3.eth.get_block('latest').baseFeePerGas
    priority_fee = web3.eth.max_priority_fee
    max_fee = priority_fee + 2 * base_fee

    build_trx_config = {
        'chainId': web3.eth.chain_id,
        'from': base_adr,
        'nonce': web3.eth.get_transaction_count(base_adr),
        # 'gasPrice': web3.eth.gas_price,
        'maxFeePerGas': max_fee,  # 30000000000,
        'maxPriorityFeePerGas': priority_fee  # 3000000000,
    }
    gas_eddition = 1000
    #if infura_url.find("infura") != -1:
    #    gas_eddition = 1000
    gas = web3.eth.estimate_gas(build_trx_config) + gas_eddition
    build_trx_config['gas'] = gas + int(gas * 0.1)

    return build_trx_config


def call_func_sc_confirm_trx(adr_of_owner):
    web3 = Web3(Web3.HTTPProvider(infura_url, request_kwargs={'timeout': 60}))
    #address_contract = goerli_ms_sc_adr
    address_contract = sibr_ms_sc_adr
    abi = ms_sc_abi
    contract = web3.eth.contract(address=web3.to_checksum_address(address_contract), abi=abi)

    build_trx_config = {
        'chainId': web3.eth.chain_id,
        'from': adr_of_owner,
        'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.get_transaction_count(adr_of_owner)
    }
    gas = web3.eth.estimate_gas(build_trx_config) + 200000
    build_trx_config['gas'] = gas + int(gas * 0.2)

    f = contract.functions.confirmTransaction(0)
    unsigned_tx = f.build_transaction(build_trx_config)
    signed_tx = web3.eth.account.sign_transaction(unsigned_tx, adrs_pk[adr_of_owner])
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)


def call_function_from_sc_exec_transaction():
    web3 = Web3(Web3.HTTPProvider(infura_url, request_kwargs={'timeout': 60}))
    #address_contract = goerli_ms_sc_adr
    address_contract = sibr_ms_sc_adr
    abi = ms_sc_abi
    contract = web3.eth.contract(address=web3.to_checksum_address(address_contract), abi=abi)
    print(contract.functions.getTransaction(0).call())

    build_trx_config = {
        'chainId': web3.eth.chain_id,
        'from': first_adr,
        'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.get_transaction_count(first_adr)
    }
    gas = web3.eth.estimate_gas(build_trx_config) + 200000
    build_trx_config['gas'] = gas + int(gas * 0.2)

    f = contract.functions.executeTransaction(0)
    unsigned_tx = f.build_transaction(build_trx_config)
    signed_tx = web3.eth.account.sign_transaction(unsigned_tx, first_adr_pk)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)


def call_function_from_sc():
    web3 = Web3(Web3.HTTPProvider(infura_url, request_kwargs={'timeout': 60}))

    #address_contract = goerli_ms_sc_adr
    address_contract = sibr_ms_sc_adr
    abi = ms_sc_abi
    contract = web3.eth.contract(address=web3.to_checksum_address(address_contract), abi=abi)

    print(contract.functions.numConfirmationsRequired().call())

    wei_value = web3.to_wei(0.0001, 'ether')

    build_trx_config = {
        'chainId': web3.eth.chain_id,
        'from': first_adr,
        'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.get_transaction_count(first_adr)
    }
    gas = web3.eth.estimate_gas(build_trx_config) + 200000
    build_trx_config['gas'] = gas + int(gas*0.2)

    f = contract.functions.submitTransaction(third_adr, int(wei_value), bytearray())
    #f.call(build_trx_config)
    #
    unsigned_tx = f.build_transaction(build_trx_config)
    signed_tx = web3.eth.account.sign_transaction(unsigned_tx, first_adr_pk)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)
    # tx = f.build_transaction(build_trx_config)
    # tx_hash = web3.eth.call(tx)


def get_owner_from_sc(sc_address, sc_abi):
    web3 = Web3(Web3.HTTPProvider(infura_url, request_kwargs={'timeout': 60}))
    contract = web3.eth.contract(address=web3.to_checksum_address(sc_address), abi=sc_abi)
    print(contract.functions.owner().call())
    return


def set_owner_to_sc(new_owner_adr, sc_adr, sc_abi):
    web3 = Web3(Web3.HTTPProvider(infura_url, request_kwargs={'timeout': 60}))
    contract = web3.eth.contract(address=web3.to_checksum_address(sc_adr), abi=sc_abi)

    build_trx_config = standard_trx_build_for_sc_call_with_gas()
    f = contract.functions.setOwner(web3.to_checksum_address(new_owner_adr))
    unsigned_tx = f.build_transaction(build_trx_config)
    signed_tx = web3.eth.account.sign_transaction(unsigned_tx, first_adr_pk)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)

    print(f"owner after set = {contract.functions.owner().call()}")


def mint_tokens(sc_address, sc_abi):
    web3 = Web3(Web3.HTTPProvider(infura_url, request_kwargs={'timeout': 60}))
    contract = web3.eth.contract(address=web3.to_checksum_address(sc_address), abi=sc_abi)

    #print(f"before mint supply = {contract.functions.totalSupply().call()}")

    build_trx_config = {
        'chainId': web3.eth.chain_id,
        'from': first_adr,
        'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.get_transaction_count(first_adr)
    }
    gas = web3.eth.estimate_gas(build_trx_config) + 100000
    build_trx_config['gas'] = gas + int(gas * 0.2)

    recepient_adr = "0xa7b10B62261BBc84d86D46a65647D2a6Becf281d"
    f = contract.functions.mintAndTransferIssue(web3.to_checksum_address(recepient_adr), int(web3.to_wei(0.007, 'ether')), 27)
    unsigned_tx = f.build_transaction(build_trx_config)
    signed_tx = web3.eth.account.sign_transaction(unsigned_tx, first_adr_pk)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)

    #print(f"after mint supply = {contract.functions.totalSupply().call()}")


def balance_of_adr_in_tokens(check_adr, tokens_sc_adr, sc_abi):
    web3 = Web3(Web3.HTTPProvider(infura_url, request_kwargs={'timeout': 60}))
    contract = web3.eth.contract(address=web3.to_checksum_address(tokens_sc_adr), abi=sc_abi)

    print(f"balance of adr = {contract.functions.balanceOf(web3.to_checksum_address(check_adr)).call()}")
    print(f"total supply = {contract.functions.totalSupply().call()}")


def ms_sc_num_req_signs(sc_address, sc_abi):
    web3 = Web3(Web3.HTTPProvider(infura_url, request_kwargs={'timeout': 60}))
    contract = web3.eth.contract(address=web3.to_checksum_address(sc_address), abi=sc_abi)

    print(f"numSignsRequired = {contract.functions.numSignsRequired().call()}")


def init_issue(sc_address, sc_abi):
    web3 = Web3(Web3.HTTPProvider(infura_url, request_kwargs={'timeout': 60}))
    contract = web3.eth.contract(address=web3.to_checksum_address(sc_address), abi=sc_abi)
    build_trx_config = standard_trx_build_for_sc_call_with_gas()
    build_trx_config['gas'] *= 5

    wei_value = web3.to_wei(0.006020, 'ether')

    f = contract.functions.initIssue(first_adr, int(wei_value))
    unsigned_tx = f.build_transaction(build_trx_config)
    signed_tx = web3.eth.account.sign_transaction(unsigned_tx, first_adr_pk)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)


def get_issue(issue_num, sc_address, sc_abi):
    web3 = Web3(Web3.HTTPProvider(infura_url, request_kwargs={'timeout': 60}))
    contract = web3.eth.contract(address=web3.to_checksum_address(sc_address), abi=sc_abi)
    print(f"get_issue = {contract.functions.getIssue(issue_num).call()}")


def sign_issue(issue_num, adr_of_owner, sc_address, sc_abi):
    web3 = Web3(Web3.HTTPProvider(infura_url, request_kwargs={'timeout': 60}))
    contract = web3.eth.contract(address=web3.to_checksum_address(sc_address), abi=sc_abi)

    build_trx_config = standard_trx_build_for_sc_call_with_gas(adr_of_owner)
    build_trx_config['gas'] += int(build_trx_config['gas'] * 0.2)

    f = contract.functions.signIssue(issue_num)
    unsigned_tx = f.build_transaction(build_trx_config)
    signed_tx = web3.eth.account.sign_transaction(unsigned_tx, adrs_pk[adr_of_owner])
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)


def provide_issue(issue_num, adr_of_owner, sc_address, sc_abi):
    web3 = Web3(Web3.HTTPProvider(infura_url, request_kwargs={'timeout': 60}))
    contract = web3.eth.contract(address=web3.to_checksum_address(sc_address), abi=sc_abi)

    build_trx_config = standard_trx_build_for_sc_call_with_gas(adr_of_owner)
    build_trx_config['gas'] *= 2

    f = contract.functions.provideIssue(issue_num)
    unsigned_tx = f.build_transaction(build_trx_config)
    signed_tx = web3.eth.account.sign_transaction(unsigned_tx, adrs_pk[adr_of_owner])
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)


def call_from_sc():
    web3 = Web3(Web3.HTTPProvider(infura_url, request_kwargs={'timeout': 60}))

    #address_contract = goerli_ms_sc_adr
    address_contract = sibr_ms_sc_adr
    abi = ms_sc_abi
    contract = web3.eth.contract(address=web3.to_checksum_address(address_contract), abi=abi)

    print(contract.functions.numConfirmationsRequired().call())

    wei_value = web3.to_wei(0.0001, 'ether')

    build_trx_config = {
        'chainId': web3.eth.chain_id,
        'from': first_adr,
        'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.get_transaction_count(first_adr)
    }
    gas = web3.eth.estimate_gas(build_trx_config) + 200000
    build_trx_config['gas'] = gas + int(gas*0.2)

    f = contract.functions.submitTransaction(third_adr, int(wei_value), bytearray())
    #f.call(build_trx_config)
    #
    unsigned_tx = f.build_transaction(build_trx_config)
    signed_tx = web3.eth.account.sign_transaction(unsigned_tx, first_adr_pk)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)
    # tx = f.build_transaction(build_trx_config)
    # tx_hash = web3.eth.call(tx)


def load_contract(cs):
    web3 = Web3(Web3.HTTPProvider(infura_url, request_kwargs={'timeout': 60}))

    contract_id, contract_interface = cs.popitem()
    # get abi
    abi = contract_interface['abi']
    # get bytecode / bin
    bytecode = contract_interface['bin']

    # set pre-funded account as sender
    web3.eth.default_account = first_adr

    ctr = web3.eth.contract(abi=abi, bytecode=bytecode)

    build_trx_config = {
        'chainId': web3.eth.chain_id,
        'from': web3.to_checksum_address(first_adr),
        'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.get_transaction_count(first_adr)
    }
    gas_eddition = 3200000

    gas = web3.eth.estimate_gas(build_trx_config) + gas_eddition
    build_trx_config['gas'] = gas

    called_constructor = ctr.constructor([second_adr, third_adr], 2, 2)
    #called_constructor = ctr.constructor()
    # .buildTransaction(tx_dict)
    tx = called_constructor.build_transaction(build_trx_config)

    signed_tx = web3.eth.account.sign_transaction(tx, first_adr_pk)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    print(tx_receipt)


def get_last_msw_issue(sc_address, sc_abi) -> int:
    web3 = Web3(Web3.HTTPProvider(infura_url, request_kwargs={'timeout': 60}))
    contract = web3.eth.contract(address=web3.to_checksum_address(sc_address), abi=sc_abi)
    last_issue = contract.functions.getIssuesCount().call()
    print(f"last issue = {last_issue}")
    return int(last_issue)


def make_transaction(from_adr=first_adr, to_adr=second_adr, value=0.0001):
    web3 = Web3(Web3.HTTPProvider(infura_url, request_kwargs={'timeout': 60}))

    tx_dict = standard_trx_build_for_usual_trans()

    tx_dict['to'] = web3.to_checksum_address(to_adr)
    tx_dict['value'] = web3.to_wei(value, 'ether')

    signed_tx = web3.eth.account.sign_transaction(tx_dict, adrs_pk[from_adr])
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)


def make_token_transfer(_from, _to, token_sc_adr, token_sc_abi):
    web3 = Web3(Web3.HTTPProvider(infura_url, request_kwargs={'timeout': 60}))
    contract = web3.eth.contract(address=web3.to_checksum_address(token_sc_adr), abi=token_sc_abi)

    build_trx_config = standard_trx_build_for_sc_call_with_gas(_from)

    f = contract.functions.transfer(web3.to_checksum_address(_to), int(web3.to_wei(0.0001, 'ether')))
    unsigned_tx = f.build_transaction(build_trx_config)
    signed_tx = web3.eth.account.sign_transaction(unsigned_tx, adrs_pk[_from])
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)


def make_token_transfer_from(_from, _to, token_sc_adr, token_sc_abi):
    web3 = Web3(Web3.HTTPProvider(infura_url, request_kwargs={'timeout': 60}))
    contract = web3.eth.contract(address=web3.to_checksum_address(token_sc_adr), abi=token_sc_abi)

    build_trx_config = standard_trx_build_for_sc_call_with_gas(_from)

    f = contract.functions.transferFrom(web3.to_checksum_address(_from),
                                        web3.to_checksum_address(_to),
                                        int(web3.to_wei(0.0003, 'ether')))
    unsigned_tx = f.build_transaction(build_trx_config)
    signed_tx = web3.eth.account.sign_transaction(unsigned_tx, adrs_pk[_from])
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)


def test():
    print("hello")


#sibr_weths_v8_adr = '0x6d7e26774aB7cEf9EE9Ca55CB7BA5922605DD182'
sibr_weths_v9_adr = "0xfa9CaD4Ab2BC505e805986fC27e1c6A44853E2CD"
sibr_msw_issuer_v6_adr = "0x3A8C0C5C1e7CADce605f57Eee2104e5dbdC9e13C"

goerli_wsibr_v9_adr = '0xA72d39Ac1c5BB0abc1A044741947ACC44a23CCe5'
goerli_msw_issuer_v6_adr = "0x013538B357A4c2CcdE81E2318e5cA0560c171C8e"

goerli_ms_sc_adr = '0x8b9c40d3518c167c25cc999f31370d9e6f5b0859'
goerli_ms_sc_abi = '[{"inputs":[{"internalType":"address[]","name":"_guardians","type":"address[]"},{"internalType":"uint256","name":"_numConfirmationsRequired","type":"uint256"},{"internalType":"uint256","name":"_numSignsRequired","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"guardianOne","type":"address"},{"indexed":true,"internalType":"address","name":"guardianTwo","type":"address"}],"name":"ChoosenGuardiansEvent","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"uint256","name":"txIndex","type":"uint256"}],"name":"ConfirmTransaction","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"balance","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"uint256","name":"txIndex","type":"uint256"}],"name":"ExecuteTransaction","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"uint256","name":"issueIndex","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"IssueInited","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"uint256","name":"issueIndex","type":"uint256"}],"name":"IssueProvided","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"uint256","name":"issueIndex","type":"uint256"}],"name":"IssueSigned","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"uint256","name":"txIndex","type":"uint256"}],"name":"RevokeConfirmation","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"uint256","name":"txIndex","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"},{"indexed":false,"internalType":"bytes","name":"data","type":"bytes"}],"name":"SubmitTransaction","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"WrapTokensReceived","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"message","type":"string"},{"indexed":false,"internalType":"uint256","name":"num","type":"uint256"}],"name":"logstr","type":"event"},{"inputs":[],"name":"WETHTokenAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"WrappedTokenAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"},{"internalType":"uint256","name":"issueIndex","type":"uint256"}],"name":"callMintWSIBR","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_txIndex","type":"uint256"}],"name":"confirmTransaction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_txIndex","type":"uint256"}],"name":"executeTransaction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getGuardians","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_issueIndex","type":"uint256"}],"name":"getIssue","outputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bool","name":"provided","type":"bool"},{"internalType":"uint256","name":"numSigns","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getIssuesCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getOwners","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_txIndex","type":"uint256"}],"name":"getTransaction","outputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"bool","name":"executed","type":"bool"},{"internalType":"uint256","name":"numConfirmations","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTransactionCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"guardians","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"initIssue","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"name":"isConfirmed","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"isGuardian","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"name":"isSigned","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"issueRewardPercent","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"issues","outputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"signersReward","type":"uint256"},{"internalType":"bool","name":"provided","type":"bool"},{"internalType":"uint256","name":"numSigns","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"numConfirmationsRequired","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"numSignsRequired","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_issueIndex","type":"uint256"}],"name":"provideIssue","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"provider","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amountTokens","type":"uint256"}],"name":"recvWrapCoinsBack","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_txIndex","type":"uint256"}],"name":"revokeConfirmation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_issueIndex","type":"uint256"}],"name":"signIssue","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"signersRewardPercent","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"submitTransaction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"transactions","outputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"bool","name":"executed","type":"bool"},{"internalType":"uint256","name":"numConfirmations","type":"uint256"}],"stateMutability":"view","type":"function"},{"stateMutability":"payable","type":"receive"}]'

weth_goerli_adr = "0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6"
weth_goerli_abi='[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"guy","type":"address"},{"name":"wad","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"src","type":"address"},{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"wad","type":"uint256"}],"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"deposit","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"guy","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Withdrawal","type":"event"}]'

if __name__ == '__main__':
    test()
    #make_token_transfer_from(first_adr, goerli_msw_issuer_v6_adr, weth_goerli_adr, weth_goerli_abi)
    #make_transaction(first_adr, "0x7361ee4Cce328E956B2d4c42623A2570AEdf0fA7", 0.02002)
    #make_transaction(first_adr, sibr_msw_issuer_v6_adr, 0.0101)
    #make_transaction(first_adr, sibr_msw_issuer_v6_adr, 0.0103)
    #make_transaction(first_adr, goerli_ms_sc_adr, 0.01)
    #make_transaction(first_adr, goerli_msw_issuer_v6_adr, 0.01004)
    #make_transaction(first_adr, second_adr, 0.1731)
    #make_transaction(first_adr, third_adr, 0.0001)
    #c_sc = compiled_sibr_weth_v9

    #c_sc = compiled_goerli_msw_issue_v6
    #c_sc = compiled_sibr_msw_issue_v6
    #contract_id, contract_interface = c_sc.popitem()

    #contract_id, contract_interface = c_sc.popitem()
    #abi = contract_interface['abi']

    #make_token_transfer(first_adr, second_adr, weths_v7_sc_adr, abi)
    #init_issue(goerli_msw_issuer_v6_adr, abi)
    init_issue(goerli_ms_sc_adr, goerli_ms_sc_abi)
    #issue_num = get_last_msw_issue(goerli_msw_issuer_v6_adr, abi) - 1
    #get_issue(25, sibr_msw_issuer_v6_adr, abi)
    #sign_issue(2, second_adr, goerli_msw_issuer_v6_adr, abi)
    # sign_issue(issue_num, second_adr, msw_issue_mint_v3_adr, abi)
    #provide_issue(25, first_adr, goerli_msw_issuer_v6_adr, abi)
    # get_issue(issue_num, msw_issue_mint_v3_adr, abi)
    #get_owner_from_sc(sibr_weths_v9_adr, abi)
    #set_owner_to_sc(sibr_msw_issuer_v4_adr, sibr_weths_v9_adr, abi)
    #get_owner_from_sc(sibr_weths_v9_adr, abi)
    #mint_tokens(sibr_weths_v9_adr, abi)
    #balance_of_adr_in_tokens(third_adr, weths_v7_sc_adr, abi)
    #call_func_sc_confirm_trx(first_adr)
    #call_func_sc_confirm_trx(second_adr)
    #call_function_from_sc_exec_transaction()
    #call_function_from_sc()
    #load_contract(c_sc)
