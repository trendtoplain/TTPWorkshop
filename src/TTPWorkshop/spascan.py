from ws.scan.spaddressscan import(
    sp_address_scan
)

from ws.generator.pkeys import(
    PKeysFactory
)
 
kf = PKeysFactory()

start = kf.produce(64)
scancount = 100000000
sp_address_scan(start, scancount, True, -1)
