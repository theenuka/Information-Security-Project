import argparse
from pprint import pprint
from config import KEY, SAMPLES
from chaos_aes.experiment import run


def main():
    p = argparse.ArgumentParser(description="AES-128 S-Box modification experiment")
    p.add_argument("--samples", type=int, default=SAMPLES)
    p.add_argument("--out", default="results/report.csv")
    args = p.parse_args()
    pprint(run(KEY, args.samples, args.out), sort_dicts=False)


if __name__ == "__main__":
    main()
