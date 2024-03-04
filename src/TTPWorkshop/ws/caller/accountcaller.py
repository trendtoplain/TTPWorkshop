from web3 import Web3
 
from ws.utils.jacobian import(  
    produce_wallet
)

from ws.net import(
    get_web3
)

from ws.chains.ChainIds import (
    BSC
)

class AccountCaller:
    def __init__(self, private_key, chainid=BSC):
        self.private_key = private_key
        self.address =  Web3.toChecksumAddress(produce_wallet(private_key))
        self.chainid = chainid
        self.w3 = get_web3(chainid)

    def change_net(self, chainid):
       if(chainid != chainid):
           self.chainid = chainid
           self.w3 = get_web3(chainid)

    def balance(self):
        value = self.w3.eth.getBalance(self.address)
        return Web3.fromWei(value, 'ether')

    def nonce(self):
        return self.w3.eth.getTransactionCount(self.address)

    def transfer(self, to, amount, gas=21000, code=b'', nonce=-1):
        value = Web3.toWei(amount, 'ether')
        to = Web3.toChecksumAddress(to)
        nonce=self.w3.eth.getTransactionCount(self.address) if (nonce < 0) else nonce
        signed_txn = self.w3.eth.account.signTransaction(dict(
            nonce=nonce,
            gasPrice=self.w3.eth.gasPrice,
            gas=gas,
            to=to,
            value=value,
            data=code,
            chainId=self.chainid
            ), self.private_key)

        try:
            self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            print('success')
        except Exception as e:
            print(str(e))

    def create(self, code, gas=8000000):
        signed_txn = self.w3.eth.account.signTransaction(dict(
            nonce=self.w3.eth.getTransactionCount(self.address),
            gasPrice=self.w3.eth.gasPrice,
            gas=8000000,
            data=code,
            chainId=self.chainid), self.private_key)
        try:
            self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            print('success')
        except Exception as e:
            print(str(e))

 
    
   
    
