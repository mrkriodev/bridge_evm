import os
import logging
import time
from web3 import Web3
from compiled_contracts.goerli_wsibr_v8_minted_compiled import compiled_goerli_wsibr_v8
from compiled_contracts.goerli_msw_issue_v4 import compiled_goerli_msw_issue_v4
from compiled_contracts.sibr_weth_v8_compiled import compiled_sibr_weth_v8
from compiled_contracts.sibr_msw_issue_v4 import compiled_sibr_msw_issue_v4

logging.basicConfig(level=logging.DEBUG)
IS_INFURA = False
#infura_url = 'https://goerli.infura.io/v3/8596c2e3a7704213911e675a8eedd635'
infura_url = 'https://rpc.test.siberium.net'
first_adr = '0xade657554299E886Fb0150d4293D441f278A9854'
second_adr = '0xc6322A3D73f791dFf977984F5380468885Beed77'
third_adr = '0xe52FB548417eE451192200fdAf8Fa1511daB2300'
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


def standard_trx_build_for_sc_call_with_gas(base_adr=None) -> dict:
    if base_adr is None:
        base_adr = first_adr
    web3 = Web3(Web3.HTTPProvider(infura_url, request_kwargs={'timeout': 60}))

    build_trx_config = {
        'chainId': web3.eth.chain_id,
        'from': base_adr,
        'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.get_transaction_count(base_adr)
    }
    gas_eddition = 0
    if not IS_INFURA:
        gas_eddition = 100000
    gas = web3.eth.estimate_gas(build_trx_config) + gas_eddition
    build_trx_config['gas'] = gas + int(gas * 0.2)

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

    f = contract.functions.mintAndTransfer(web3.to_checksum_address(first_adr), int(web3.to_wei(0.0033, 'ether')))
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

    wei_value = web3.to_wei(0.0001, 'ether')

    f = contract.functions.initIssue(third_adr, int(wei_value))
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
    gas_eddition = 3000000

    gas = web3.eth.estimate_gas(build_trx_config) + gas_eddition
    build_trx_config['gas'] = gas

    called_constructor = ctr.constructor([first_adr, second_adr], 2)
    #called_constructor = ctr.constructor()
    # .buildTransaction(tx_dict)
    tx = called_constructor.build_transaction(build_trx_config)

    signed_tx = web3.eth.account.sign_transaction(tx, first_adr_pk)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    print(tx_receipt)


def get_last_msw_issue(sc_address, sc_abi):
    web3 = Web3(Web3.HTTPProvider(infura_url, request_kwargs={'timeout': 60}))
    contract = web3.eth.contract(address=web3.to_checksum_address(sc_address), abi=sc_abi)
    return contract.functions.getIssuesCount().call()


def make_transaction(from_adr=first_adr, to_adr=second_adr, value=0.0001):
    web3 = Web3(Web3.HTTPProvider(infura_url, request_kwargs={'timeout': 60}))

    tx_dict = {
        'chainId': web3.eth.chain_id,
        'from': web3.to_checksum_address(from_adr),
        'to': web3.to_checksum_address(to_adr),
        'nonce': web3.eth.get_transaction_count(from_adr),
        'value': web3.to_wei(value, 'ether'),
        'gasPrice': web3.eth.gas_price,
    }

    gas_eddition = 0
    if not IS_INFURA:
        gas_eddition = 100000

    gas = web3.eth.estimate_gas(tx_dict) + gas_eddition
    tx_dict['gas'] = gas + int(gas*0.2)

    signed_tx = web3.eth.account.sign_transaction(tx_dict, adrs_pk[from_adr])
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)


def make_token_transfer(_from, _to, token_sc_adr, token_sc_abi):
    web3 = Web3(Web3.HTTPProvider(infura_url, request_kwargs={'timeout': 60}))
    contract = web3.eth.contract(address=web3.to_checksum_address(token_sc_adr), abi=token_sc_abi)

    build_trx_config = standard_trx_build_for_sc_call_with_gas(_from)

    f = contract.functions.transfer(web3.to_checksum_address(_to), int(web3.to_wei(0.003, 'ether')))
    unsigned_tx = f.build_transaction(build_trx_config)
    signed_tx = web3.eth.account.sign_transaction(unsigned_tx, adrs_pk[_from])
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)


def test():
    print("hello")


sibr_weths_v8_adr = '0x6d7e26774aB7cEf9EE9Ca55CB7BA5922605DD182'
sibr_msw_issuer_v4_adr = '0x14DE0EAe16cFd97Eb19e4a97d82Dad72E02D6A8A'

goerli_wsibr_v8_adr = '0xac2ff53d3329f0aa57a23daff393704dc4f30d7d'
goerli_msw_issuer_v4_adr = '0xD9FeF2B97B52082711fBDF4fB99670E717e599c1'


if __name__ == '__main__':
    test()
    #make_transaction(fourth_adr, first_adr, 0.09570947275)
    c_sc = compiled_sibr_weth_v8
    #c_sc = compiled_sibr_msw_issue_v4
    #c_sc = compiled_goerli_wsibr_v8
    #c_sc = compiled_goerli_msw_issue_v4
    contract_id, contract_interface = c_sc.popitem()
    #contract_id, contract_interface = c_sc.popitem()
    abi = contract_interface['abi']
    #make_token_transfer(first_adr, second_adr, weths_v7_sc_adr, abi)
    # init_issue(msw_issue_mint_v3_adr, abi)
    # issue_num = get_last_msw_issue(msw_issue_mint_v3_adr, abi) - 1
    # get_issue(issue_num, msw_issue_mint_v3_adr, abi)
    # sign_issue(issue_num, first_adr, msw_issue_mint_v3_adr, abi)
    # sign_issue(issue_num, second_adr, msw_issue_mint_v3_adr, abi)
    # provide_issue(issue_num, first_adr, msw_issue_mint_v3_adr, abi)
    # get_issue(issue_num, msw_issue_mint_v3_adr, abi)
    #get_owner_from_sc(sibr_weths_v8_adr, abi)
    #set_owner_to_sc(sibr_msw_issuer_v4_adr, sibr_weths_v8_adr, abi)
    #get_owner_from_sc(sibr_weths_v8_adr, abi)
    #mint_tokens(weths_v7_sc_adr, abi)
    #balance_of_adr_in_tokens(first_adr, weths_v7_sc_adr, abi)
    #balance_of_adr_in_tokens(second_adr, weths_v7_sc_adr, abi)
    #balance_of_adr_in_tokens(third_adr, weths_v7_sc_adr, abi)
    #call_func_sc_confirm_trx(first_adr)
    #call_func_sc_confirm_trx(second_adr)
    #call_function_from_sc_exec_transaction()
    #call_function_from_sc()
    #load_contract(c_sc)
