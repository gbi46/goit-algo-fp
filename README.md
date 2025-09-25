
# Run the project

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

# Dice Sums via Monte Carlo

This project simulates rolling **two fair six-sided dice** a large number of times
and estimates the probability of each possible sum (2..12). It then **compares the
Monte Carlo results** with the **analytical (exact) probabilities**.

## Method
1. Randomly generate outcomes for two dice per trial.
2. Compute the sum for each trial.
3. Count occurrences of each sum and divide by the total number of trials to get empirical probabilities.
4. Compare with the exact probabilities derived from counting outcomes (1/36, 2/36, ..., 6/36, ..., 1/36).

---

## Analytical probabilities (two fair dice)

| Sum | Probability |
|----:|------------:|
| 2   | 2.78% (1/36)  |
| 3   | 5.56% (2/36)  |
| 4   | 8.33% (3/36)  |
| 5   | 11.11% (4/36) |
| 6   | 13.89% (5/36) |
| 7   | 16.67% (6/36) |
| 8   | 13.89% (5/36) |
| 9   | 11.11% (4/36) |
| 10  | 8.33% (3/36)  |
| 11  | 5.56% (2/36)  |
| 12  | 2.78% (1/36)  |

---

## Example output (abridged)

After running rolls = 1_000_000, you will see a table like:

```
Sum |  Empirical % |  Theoretical % |  Abs Error %
  2 |       2.7800 |          2.7778 |      0.0022
  3 |       5.5650 |          5.5556 |      0.0094
  ...
  12|       2.7745 |          2.7778 |      0.0033

Error metrics:
  max_abs_error: 0.00012
  mae: 0.00005
  mse: 0.00000
  chi_square: 0.00087
```

A bar chart (`probabilities.png`) is also saved comparing empirical vs theoretical probabilities.

---

## Conclusions

- The Monte Carlo estimates **converge** to the analytical probabilities as the number of rolls grows.
- The **largest deviations** occur for sums near the tails (2 and 12) with fewer combinations.
- Error decreases roughly as **1 / √N**; increasing trials improves accuracy while increasing runtime.
- The simulation validates the analytical table above within small Monte Carlo error.
