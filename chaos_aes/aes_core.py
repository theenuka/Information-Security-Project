from .aes_tables import RCON, S_BOX
from .chaos_sbox import inverse_sbox


def xtime(a):
    return ((a << 1) ^ 0x1B) & 0xFF if a & 0x80 else a << 1


def gmul(a, b):
    p = 0
    for _ in range(8):
        if b & 1: p ^= a
        a, b = xtime(a), b >> 1
    return p


def add_round_key(s, k):
    return [x ^ y for x, y in zip(s, k)]


def sub_bytes(s, box):
    return [box[x] for x in s]


def shift_rows(s):
    return [s[0],s[5],s[10],s[15], s[4],s[9],s[14],s[3], s[8],s[13],s[2],s[7], s[12],s[1],s[6],s[11]]


def inv_shift_rows(s):
    return [s[0],s[13],s[10],s[7], s[4],s[1],s[14],s[11], s[8],s[5],s[2],s[15], s[12],s[9],s[6],s[3]]


def mix_columns(s):
    out = s[:]
    for c in range(4):
        i = 4 * c; a = s[i:i+4]
        out[i:i+4] = [gmul(a[0],2)^gmul(a[1],3)^a[2]^a[3], a[0]^gmul(a[1],2)^gmul(a[2],3)^a[3], a[0]^a[1]^gmul(a[2],2)^gmul(a[3],3), gmul(a[0],3)^a[1]^a[2]^gmul(a[3],2)]
    return out


def inv_mix_columns(s):
    out = s[:]
    for c in range(4):
        i = 4 * c; a = s[i:i+4]
        out[i:i+4] = [gmul(a[0],14)^gmul(a[1],11)^gmul(a[2],13)^gmul(a[3],9), gmul(a[0],9)^gmul(a[1],14)^gmul(a[2],11)^gmul(a[3],13), gmul(a[0],13)^gmul(a[1],9)^gmul(a[2],14)^gmul(a[3],11), gmul(a[0],11)^gmul(a[1],13)^gmul(a[2],9)^gmul(a[3],14)]
    return out


def expand_key(key: bytes, sbox=S_BOX):
    if len(key) != 16: raise ValueError("AES-128 key must be 16 bytes")
    words = [list(key[i:i+4]) for i in range(0, 16, 4)]
    for i in range(4, 44):
        temp = words[-1][:]
        if i % 4 == 0:
            temp = [sbox[b] for b in temp[1:] + temp[:1]]
            temp[0] ^= RCON[i // 4]
        words.append([a ^ b for a, b in zip(words[-4], temp)])
    return [sum(words[i:i+4], []) for i in range(0, 44, 4)]


class AES128:
    def __init__(self, key: bytes, sbox=None):
        self.sbox = sbox or S_BOX
        self.inv_sbox = inverse_sbox(self.sbox)
        self.round_keys = expand_key(key, self.sbox)

    def encrypt_block(self, block: bytes) -> bytes:
        if len(block) != 16: raise ValueError("Block must be 16 bytes")
        s = add_round_key(list(block), self.round_keys[0])
        for r in range(1, 10):
            s = add_round_key(mix_columns(shift_rows(sub_bytes(s, self.sbox))), self.round_keys[r])
        return bytes(add_round_key(shift_rows(sub_bytes(s, self.sbox)), self.round_keys[10]))

    def decrypt_block(self, block: bytes) -> bytes:
        s = add_round_key(list(block), self.round_keys[10])
        for r in range(9, 0, -1):
            s = inv_mix_columns(add_round_key(sub_bytes(inv_shift_rows(s), self.inv_sbox), self.round_keys[r]))
        return bytes(add_round_key(sub_bytes(inv_shift_rows(s), self.inv_sbox), self.round_keys[0]))
