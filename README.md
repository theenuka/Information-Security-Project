# EC6204 Information Security Mini Project

## Title
Chaos-Driven Dynamic S-Box Generation for AES Using the Logistic Map: A Cryptographic Strength Enhancement Approach

This project matches the submitted proposal and the project description: select an information-security algorithm, propose a software modification, and experimentally prove the effect using appropriate metrics.

## Exact alignment with proposal

- Algorithm: AES-128
- Baseline: Standard AES with original static S-Box
- Proposed modification: Key-dependent dynamic S-Box generation using the chaotic logistic map with r = 3.99
- Integration point: AES SubBytes and AES key expansion S-Box usage
- Validation: bijection/permutation check for every generated S-Box
- Metrics: nonlinearity, Strict Avalanche Criterion error, Bit Independence Criterion error, differential uniformity, encryption throughput
- Experiment size: configurable; default is 10,000 plaintext blocks
- Exclusions: no CBC/GCM modes, no hardware implementation, no side-channel analysis

## Important design decision

A naive logistic-map S-Box is included as `raw_logistic_dynamic`. It proves that simply sorting chaotic values is not enough.

The final proposed version is `optimized_chaos_affine`. It uses chaos-derived affine-equivalent generation to preserve the strongest AES S-Box properties while allowing key-dependent dynamic substitution. This keeps nonlinearity and differential uniformity at AES level while improving avalanche-related metrics in the provided experiment.

## Run

```bash
pip install -r requirements.txt
python main.py --samples 10000
pytest
```

Fast test run:

```bash
python main.py --samples 1000
```

## Output

Results are written to:

```text
results/report.csv
```

## Viva-safe final claim

The project does not claim AES is broken. It claims that a logistic-map-driven, key-dependent dynamic S-Box can be integrated into AES-128 and experimentally evaluated. The optimized version preserves AES-level nonlinearity and differential uniformity while improving SAC and BIC error for the tested setup, without major throughput loss.
