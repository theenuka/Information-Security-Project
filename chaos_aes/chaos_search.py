import random
from .aes_tables import S_BOX
from .affine import affine_equiv_sbox, is_invertible
from .metrics import analyze_sbox, sac_error, bic_error


def random_matrix(rng: random.Random) -> list[int]:
    while True:
        rows = [rng.randrange(1, 256) for _ in range(8)]
        if is_invertible(rows):
            return rows


def score(m: dict) -> float:
    return m["sac_error"] + 0.25 * m["bic_error"]


def search(seed: int = 20260605, candidates: int = 200) -> tuple[list[int], dict]:
    rng = random.Random(seed)
    best_sbox, best_m = S_BOX[:], analyze_sbox(S_BOX)
    for _ in range(candidates):
        s = affine_equiv_sbox(S_BOX, random_matrix(rng), random_matrix(rng), rng.randrange(256), rng.randrange(256))
        quick = {"nonlinearity": 112, "sac_error": round(sac_error(s), 5), "bic_error": round(bic_error(s), 5), "differential_uniformity": 4}
        if score(quick) < score(best_m):
            best_sbox, best_m = s, quick
    return best_sbox, best_m
