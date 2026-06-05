from os import urandom


def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def chunks(data: bytes, size: int):
    for i in range(0, len(data), size):
        yield data[i:i + size]


def random_blocks(n: int) -> list[bytes]:
    return [urandom(16) for _ in range(n)]
