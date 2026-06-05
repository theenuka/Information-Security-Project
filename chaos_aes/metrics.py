import itertools
import numpy as np


def bit(x, i): return (x >> i) & 1

def walsh(values):
    arr = np.array([1 - 2 * v for v in values], dtype=int)
    h = 1
    while h < len(arr):
        for i in range(0, len(arr), h * 2):
            x, y = arr[i:i+h].copy(), arr[i+h:i+2*h].copy()
            arr[i:i+h], arr[i+h:i+2*h] = x + y, x - y
        h *= 2
    return arr


def nonlinearity(sbox):
    scores = []
    for out_bit in range(8):
        truth = [bit(sbox[x], out_bit) for x in range(256)]
        scores.append(128 - max(abs(walsh(truth))) // 2)
    return min(scores)


def sac_error(sbox):
    probs = []
    for in_bit in range(8):
        for out_bit in range(8):
            flips = sum(bit(sbox[x], out_bit) ^ bit(sbox[x ^ (1 << in_bit)], out_bit) for x in range(256))
            probs.append(flips / 256)
    return float(np.mean(np.abs(np.array(probs) - 0.5)))


def bic_error(sbox):
    vals = []
    for in_bit in range(8):
        for a, b in itertools.combinations(range(8), 2):
            pa = np.array([bit(sbox[x], a) ^ bit(sbox[x ^ (1 << in_bit)], a) for x in range(256)])
            pb = np.array([bit(sbox[x], b) ^ bit(sbox[x ^ (1 << in_bit)], b) for x in range(256)])
            vals.append(abs(np.corrcoef(pa, pb)[0, 1]))
    return float(np.nanmean(vals))


def differential_uniformity(sbox):
    best = 0
    for dx in range(1, 256):
        counts = [0] * 256
        for x in range(256):
            counts[sbox[x] ^ sbox[x ^ dx]] += 1
        best = max(best, max(counts))
    return best


def analyze_sbox(sbox):
    return {
        "nonlinearity": int(nonlinearity(sbox)),
        "sac_error": round(sac_error(sbox), 5),
        "bic_error": round(bic_error(sbox), 5),
        "differential_uniformity": differential_uniformity(sbox),
    }
