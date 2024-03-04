from web3 import Web3
from web3.contract import ConciseContract

from ws.net import(
    get_web3
)

from ws.chains.ChainIds import (
    BSC
)

class Caller:
    def __init__(self, chainid=BSC):
        self._chainid = chainid
        self._w3 = get_web3(chainid)

    def _check_wallet(self, wallet):
        return Web3.toChecksumAddress(wallet)

    def _create_contract(self, address, abi):
        address = self._check_wallet(address)
        return self._w3.eth.contract(address=address, abi=abi)

    def _calling(self, txn_dict, wallet_key):
        try:
            signed_txn = self._w3.eth.account.signTransaction(txn_dict, private_key=wallet_key)
            self._w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            print('success!')
        except Exception as e:
            print(str(e))
