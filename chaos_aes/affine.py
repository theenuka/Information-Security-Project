def parity(x: int) -> int:
    return x.bit_count() & 1


def apply_matrix(rows: list[int], x: int) -> int:
    return sum(parity(row & x) << i for i, row in enumerate(rows))


def rank(rows: list[int]) -> int:
    rows, r = rows[:], 0
    for col in range(8):
        pivot = next((i for i in range(r, 8) if (rows[i] >> col) & 1), None)
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        for i in range(8):
            if i != r and ((rows[i] >> col) & 1):
                rows[i] ^= rows[r]
        r += 1
    return r


def is_invertible(rows: list[int]) -> bool:
    return len(rows) == 8 and rank(rows) == 8


def affine_equiv_sbox(base: list[int], a: list[int], b: list[int], in_xor: int, out_xor: int) -> list[int]:
    if not is_invertible(a) or not is_invertible(b):
        raise ValueError("Affine matrices must be invertible")
    return [apply_matrix(b, base[apply_matrix(a, x) ^ in_xor]) ^ out_xor for x in range(256)]
