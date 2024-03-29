from web3 import Web3

from ws.chains.ChainIds import (
    ETH,
    BSC,
    Polygon,
    Okex,
    Op,
    EVMOS
)

def get_web3(chainid = BSC):
    if(chainid == ETH):
        return Web3(Web3.HTTPProvider(r'https://eth1.lava.build/lava-referer-8923775d-0880-4160-9738-02d8f532fb00/'))

    if(chainid == BSC):
        return Web3(Web3.HTTPProvider(r'https://bscrpc.com'))

    if(chainid == Polygon):
        return Web3(Web3.HTTPProvider(r'https://g.w.lavanet.xyz:443/gateway/polygon1/rpc-http/4128357f84ee1802c8b39aa6e58e739b'))  

    if(chainid == EVMOS):
        return Web3(Web3.HTTPProvider(r'https://evmos.lava.build/lava-referer-8171c4e3-f5e0-4c64-990a-4947fcbe1500/'))  

    if(chainid == Okex):
        return Web3(Web3.HTTPProvider(r'https://exchainrpc.okex.org/'))

    if(chainid == Op):
        return Web3(Web3.HTTPProvider(r'https://g.w.lavanet.xyz:443/gateway/optm/rpc-http/4128357f84ee1802c8b39aa6e58e739b'))

    return None
