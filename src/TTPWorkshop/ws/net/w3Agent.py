from web3 import Web3

from ws.utils.jacobian import(
    big_endian_to_int
)

from .ethrpcs import (
    get_web3
)

from ws.chains.ChainIds import (
    BSC
)

class W3Agent:
    def __init__(self, chain=BSC):
        self._chainid = chain
        self._w3 = get_web3(chain)

    def get_chain(self):
        return self._chainid

    def set_chain(self, chain):
        if(chain != self._chainid):
            self._chainid = chain
            self._w3 = get_web3(chain)

    def get_balance(self, wallet):
        wallet = Web3.toChecksumAddress(wallet)
        return self._w3.eth.get_balance(wallet)
