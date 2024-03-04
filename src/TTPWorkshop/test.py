import os
from eth_account import Account

print(dir(Account))
c = Account.create()
print(dir(c))
print(dir(c.privateKey))
print(c.privateKey)
print(c.address)