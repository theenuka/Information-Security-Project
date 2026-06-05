import csv
from pathlib import Path
from time import perf_counter
from .aes_core import AES128
from .aes_tables import S_BOX
from .chaos_sbox import make_sbox
from .metrics import analyze_sbox
from .optimized_sbox import make_optimized_sbox
from .utils import random_blocks


def benchmark(cipher, blocks):
    start = perf_counter()
    for block in blocks:
        cipher.encrypt_block(block)
    elapsed = max(perf_counter() - start, 1e-9)
    return round((len(blocks) * 16 / 1_000_000) / elapsed, 3)


def row(name, sbox, key, blocks):
    return analyze_sbox(sbox) | {"throughput_MBps": benchmark(AES128(key, sbox), blocks), "variant": name}


def run(key: bytes, samples: int, out: str = "results/report.csv"):
    blocks = random_blocks(samples)
    rows = [
        row("standard_aes", S_BOX, key, blocks),
        row("raw_logistic_dynamic", make_sbox(key), key, blocks),
        row("optimized_logistic_dynamic", make_optimized_sbox(), key, blocks),
    ]
    Path(out).parent.mkdir(exist_ok=True)
    with open(out, "w", newline="") as f:
        writer = csv.DictWriter(f, rows[0].keys())
        writer.writeheader(); writer.writerows(rows)
    return {r.pop("variant"): r for r in rows}
