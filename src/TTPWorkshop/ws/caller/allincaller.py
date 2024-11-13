from web3 import Web3

from .caller import(
    Caller
)

from ws.abi import(
    AllInABI
)

class AllInCaller(Caller):
    def __init__(self, chainid, ca):
        Caller.__init__(self, chainid)
        self._contract = self._create_contract(ca, AllInABI)

    def push(self,  _toes, _am, key, wallet):
        addresses = []
        ams = []
        am = Web3.toWei(_am, 'ether') 
        for _to in _toes:
            addresses.append(Web3.toChecksumAddress(_to))
            ams.append(am)
        wallet = Web3.toChecksumAddress(wallet)

        call_function = self._contract.functions.push(addresses, ams).buildTransaction({
            'nonce': self._w3.eth.getTransactionCount(wallet),
            'gas': 14000000,
            'from': wallet,
            'value':am * len(ams),
            'chainId': self._chainid
            })

        signed_txn = self._w3.eth.account.signTransaction(call_function, private_key=key)
 
        try:
            self._w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            print('success')
        except Exception as e:
            print(str(e))
