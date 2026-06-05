from hashlib import sha256


def seed_from_key(key: bytes) -> float:
    digest = sha256(key).digest()
    value = int.from_bytes(digest[:8], "big") / 2**64
    return min(max(value, 1e-12), 1 - 1e-12)


def logistic_values(seed: float, count: int = 256, r: float = 3.99, warmup: int = 512) -> list[float]:
    x = seed
    for _ in range(warmup):
        x = r * x * (1 - x)
    out = []
    for _ in range(count):
        x = r * x * (1 - x)
        out.append(x)
    return out


def make_sbox(key: bytes) -> list[int]:
    values = logistic_values(seed_from_key(key))
    sbox = [i for i, _ in sorted(enumerate(values), key=lambda p: p[1])]
    if sorted(sbox) != list(range(256)):
        raise ValueError("Generated S-Box is not bijective")
    return sbox


def inverse_sbox(sbox: list[int]) -> list[int]:
    inv = [0] * 256
    for i, v in enumerate(sbox):
        inv[v] = i
    return inv
