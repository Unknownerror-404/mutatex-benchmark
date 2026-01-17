# Mutate-X Notes

## Overview
Mutate-X is a genetic variant analysis framework that generates
systematically mutated versions of base genetic sequences. It uses the
**EVO2 model** to evaluate the potential impact of each variant.

## Key Features
- **Variant Impact Prediction:** Classifies mutations as **benign** or **pathogenic**, with an associated machine learning confidence score.
- **Delta Likelihood:** Quantifies the change in confidence before and after mutation, helping measure the robustness or significance of a variant.
- **Variant IDs:** Each generated variant is assigned a unique identifier to track changes across experiments.
- **Chromosome Coverage:** Supports all 22 autosomes, as well as the X, Y, and mitochondrial (M) chromosomes.

## Purpose
Mutate-X is designed to:
- Simulate realistic genetic variations.
- Benchmark mutation-robust analysis methods.
- Generate datasets for ML evaluation.
- Understand mutation impact across chromosomes.

## Notes on Usage
- **Delta Likelihood (ΔL):**
  - Positive ΔL → confidence in pathogenicity increases after mutation.
  - Negative ΔL → confidence in pathogenicity decreases after mutation.
- Confidence scores should always be interpreted with biological context.
- Variant IDs make it easier to track and compare mutations across experiments.

## Example Table for Tracking Variants
| Variant ID | Chromosome | Mutation Type | ML Confidence (%) | Delta Likelihood | Predicted Impact |
|------------|------------|---------------|-------------------|------------------|------------------|
| VAR0001    | 1          | SNP           | 87                | +0.05            | Pathogenic       |
| VAR0002    | X          | Insertion     | 63                | -0.12            | Benign           |
| VAR0003    | M          | Deletion      | 92                | +0.08            | Pathogenic       |

> Tip: Keep this table updated during experiments to quickly visualize the effect of Mutate-X mutations on confidence scores and variant outcomes.