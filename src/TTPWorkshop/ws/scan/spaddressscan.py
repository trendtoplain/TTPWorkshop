from ws.utils.jacobian import(
    G,
    fast_multiply,
    fast_add,
    towallet,
    to_64hex,
    to_hex,
    get_hash
)

def get_spdict(splen):
    dict = { }
    index = 0
    while index < 16:
        c = to_hex(index)
        dict[c * 6] = c * splen 
        index = index + 1
    return dict

def sp_address_scan(start, max, downorup=False, startoffset=0, splen=8, gap=300000):
    dict = get_spdict(splen)
    p0 = int(start, 16) + startoffset
    g0 = fast_multiply(G, p0)
    lastgap = -gap if downorup else gap
    step = -1 if downorup else 1
    glast = fast_multiply(G, lastgap)
    gstep = fast_multiply(G, step)
    offset = 0
    lastoffset = 0
    index = 0
    while index < max:
        g0 = fast_add(g0, gstep)
        offset = offset + step
        wallet = towallet(g0)
        t = wallet[0:6]

        if(t in dict): 
            print('offset = ' + str(offset) + ' index = ' + str(index) + ' gap = ' + str(offset - lastoffset)  + '  ' + to_64hex(p0, offset))
            lastoffset = offset
            q = wallet[0:splen]
            if(q == dict[t]):
                print(to_64hex(p0, offset))
                print(wallet)
                index = index + max

            offset = offset + lastgap
            g0 = fast_add(g0, glast)

        index = index + 1

    print(to_64hex(p0, offset))
