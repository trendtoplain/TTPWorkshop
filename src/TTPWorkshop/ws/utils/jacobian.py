from typing import Tuple  # noqa: F401

from eth_utils import (
    keccak,
)

import codecs
import rlp

P = 2**256 - 2**32 - 977  # type: int

N = 115792089237316195423570985008687907852837564279074904382605163141518161494337  # type: int  # noqa: E501

A = 0  # type: int  # noqa: E501

B = 7  # type: int  # noqa: E501

Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240  # type: int  # noqa: E501

Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424  # type: int  # noqa: E501

G = (Gx, Gy)  # type: Tuple[int, int]

def fast_minus(g1:(int,int), g2:(int, int)) -> (int,int):
    g3 = (g2[0], P - g2[1])
    return fast_add(g1, g3)

def minus(g1:(int, int)) -> (int, int):
    return (g1[0], P - g1[1])

def produce_contract_address_create2(address, salt, initcode):
    result = produce_contract_address_create2full(address, salt, initcode)
    return result[-40:] 

def produce_contract_address_create2full(address, salt, initcode):
    message = 'ff' + address + salt + initcode
    return get_hash(message)

def get_hash(message):
    message_bytes = codecs.decode(message, 'hex')
    full_bytes = keccak(message_bytes)
    return to_64(full_bytes) 

def public_key_bytes_to_address(public_key_bytes: bytes) -> bytes:
    return keccak(public_key_bytes)

def int_to_byte(value: int) -> bytes:
    return bytes([value])

def pad32(value: bytes) -> bytes:
    return value.rjust(32, b'\x00')

def towallet(g0:(int,int)) -> str:
    public_key = encode_raw_public_key(g0)
    fulladress = public_key_bytes_to_address(public_key)
    return to_40_raw(fulladress)

def produce_wallet(private_key: str) -> str:
    r = int(private_key, 16)
    return produce_wallet_int(r)

def produce_wallet_int(private_key: int) -> str:
    gx = fast_multiply(G, private_key)
    return towallet(gx)

def decode_public_key(public_key_bytes: bytes) -> Tuple[int, int]:
    left = big_endian_to_int(public_key_bytes[0:32])
    right = big_endian_to_int(public_key_bytes[32:64])
    return left, right

def encode_raw_public_key(raw_public_key: Tuple[int, int]) -> bytes:
    left, right = raw_public_key
    return b''.join((
        pad32(int_to_big_endian(left)),
        pad32(int_to_big_endian(right)),
    ))

def private_key_to_public_key(private_key_bytes: bytes) -> bytes:
    private_key_as_num = big_endian_to_int(private_key_bytes)

    if private_key_as_num >= N:
        raise Exception("Invalid privkey")

    raw_public_key = fast_multiply(G, private_key_as_num)
    public_key_bytes = encode_raw_public_key(raw_public_key)
    return public_key_bytes

def int_to_big_endian(value: int) -> bytes:
    return value.to_bytes((value.bit_length() + 7) // 8 or 1, "big")

def big_endian_to_int(value: bytes) -> int:
    return int.from_bytes(value, "big")

def to_64hex(x:int, y = 0) -> str:
    _v = x + y
    return '{:064x}'.format(_v)[-64:]

def to_40hex(x:int, y = 0) -> str:
    _v = x + y
    return '{:040x}'.format(_v)[-40:]

def to_hex(x:int, y = 0) -> str:
    _v = x + y
    return '{:0x}'.format(_v)

def to_40(value: bytes) -> str:
    _v = big_endian_to_int(value)
    return '0x' + '{:064x}'.format(_v)[-40:]

def to_40_raw(value: bytes) -> str:
    _v = big_endian_to_int(value)
    return '{:064x}'.format(_v)[-40:]

def to_64(value: bytes) -> str:
    _v = big_endian_to_int(value)
    return  '{:064x}'.format(_v)

def inv(a: int, n: int) -> int:
    if a == 0:
        return 0
    lm, hm = 1, 0
    low, high = a % n, n
    while low > 1:
        r = high // low
        nm, new = hm - lm * r, high - low * r
        lm, low, hm, high = nm, new, lm, low
    return lm % n

def to_jacobian(p: Tuple[int, int]) -> Tuple[int, int, int]:
    o = (p[0], p[1], 1)
    return o

def jacobian_double(p: Tuple[int, int, int]) -> Tuple[int, int, int]:
    if not p[1]:
        return (0, 0, 0)
    ysq = (p[1] ** 2) % P
    S = (4 * p[0] * ysq) % P
    M = (3 * p[0] ** 2 + A * p[2] ** 4) % P
    nx = (M**2 - 2 * S) % P
    ny = (M * (S - nx) - 8 * ysq ** 2) % P
    nz = (2 * p[1] * p[2]) % P
    return (nx, ny, nz)

def jacobian_add(p: Tuple[int, int, int],
                 q: Tuple[int, int, int]) -> Tuple[int, int, int]:
    if not p[1]:
        return q
    if not q[1]:
        return p
    U1 = (p[0] * q[2] ** 2) % P
    U2 = (q[0] * p[2] ** 2) % P
    S1 = (p[1] * q[2] ** 3) % P
    S2 = (q[1] * p[2] ** 3) % P
    if U1 == U2:
        if S1 != S2:
            return (0, 0, 1)
        return jacobian_double(p)
    H = U2 - U1
    R = S2 - S1
    H2 = (H * H) % P
    H3 = (H * H2) % P
    U1H2 = (U1 * H2) % P
    nx = (R ** 2 - H3 - 2 * U1H2) % P
    ny = (R * (U1H2 - nx) - S1 * H3) % P
    nz = (H * p[2] * q[2]) % P
    return (nx, ny, nz)

def from_jacobian(p: Tuple[int, int, int]) -> Tuple[int, int]:
    z = inv(p[2], P)
    return ((p[0] * z**2) % P, (p[1] * z**3) % P)

def jacobian_multiply(a: Tuple[int, int, int],
                      n: int) -> Tuple[int, int, int]:
    if a[1] == 0 or n == 0:
        return (0, 0, 1)
    if n == 1:
        return a
    if n < 0 or n >= N:
        return jacobian_multiply(a, n % N)
    if (n % 2) == 0:
        return jacobian_double(jacobian_multiply(a, n // 2))
    elif (n % 2) == 1:
        return jacobian_add(jacobian_double(jacobian_multiply(a, n // 2)), a)
    else:
        raise Exception("Invariant: Unreachable code path")

def fast_multiply(a: Tuple[int, int],
                  n: int) -> Tuple[int, int]:
    return from_jacobian(jacobian_multiply(to_jacobian(a), n))

def fast_add(a: Tuple[int, int],
             b: Tuple[int, int]) -> Tuple[int, int]:
    return from_jacobian(jacobian_add(to_jacobian(a), to_jacobian(b)))
