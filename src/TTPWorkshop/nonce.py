from ws.utils.jacobian import(  
    produce_wallet
)

from ws.caller import(
    AccountCaller
)

import argparse

def execute(args):
    wallet_key = args.privateKey
    wallet = produce_wallet(wallet_key)
    caller = AccountCaller(wallet_key, args.cid)
    caller.transfer(args.to, args.amount, args.code, args.gas, args.nonce)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter) 
    parser.add_argument('-p', dest='privateKey', help='private key')
    parser.add_argument('-cid', dest='cid', default=1, type=int, help='chain id')
    parser.add_argument('-gas', dest='gas', default=21000, type=int, help='gas')
    parser.add_argument('-n', dest='nonce',  default=-1, type=int, help='nonce')
    parser.add_argument('-am', dest='amount', default=0, type=float, help='amount')
    parser.add_argument('-to', dest='to', help='to')
    parser.add_argument('-code', dest='code', default='', help='code')
    args = parser.parse_args()
    execute(args)
   
 
 
