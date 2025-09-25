import numpy as np
import matplotlib.pyplot as plt


def theoretical_probabilities():
    """Return a dict of theoretical probabilities for sums 2..12."""
    counts = {
        2: 1, 3: 2, 4: 3, 5: 4, 6: 5,
        7: 6,
        8: 5, 9: 4, 10: 3, 11: 2, 12: 1
    }
    total = 36
    return {s: c / total for s, c in counts.items()}


def simulate_two_dice(n_rolls, seed=None):
    """Simulate rolling two fair six-sided dice n_rolls times."""
    rng = np.random.default_rng(seed)
    die1 = rng.integers(1, 7, size=n_rolls)
    die2 = rng.integers(1, 7, size=n_rolls)
    sums = die1 + die2

    uniq, counts = np.unique(sums, return_counts=True)
    probs = {int(u): cnt / n_rolls for u, cnt in zip(uniq, counts) if 2 <= u <= 12}

    for s in range(2, 13):
        probs.setdefault(s, 0.0)
    return probs, sums


def compare_probabilities(empirical, theoretical):
    """Compute error metrics between empirical and theoretical probabilities."""
    sums = list(range(2, 13))
    emp = np.array([empirical[s] for s in sums], dtype=float)
    th = np.array([theoretical[s] for s in sums], dtype=float)

    diff = emp - th
    return {
        "max_abs_error": float(np.max(np.abs(diff))),
        "mae": float(np.mean(np.abs(diff))),
        "mse": float(np.mean(diff ** 2)),
        "chi_square": float(np.sum((diff ** 2) / th)),
    }


def print_table(empirical, theoretical):
    """Pretty-print a comparison table."""
    print("\nProbability of sums for two fair dice (Monte Carlo vs Analytical)\n")
    print(f"{'Sum':>3} | {'Empirical %':>12} | {'Theoretical %':>15} | {'Abs Error %':>11}")
    print("-" * 52)
    for s in range(2, 13):
        e = empirical[s] * 100
        t = theoretical[s] * 100
        print(f"{s:>3} | {e:12.4f} | {t:15.4f} | {abs(e - t):11.4f}")


def save_plot(empirical, theoretical, out_path="probabilities.png"):
    """Save a bar chart of empirical vs theoretical probabilities."""
    sums = np.arange(2, 13)
    emp = np.array([empirical[s] for s in sums])
    th = np.array([theoretical[s] for s in sums])

    plt.figure(figsize=(8, 5))
    width = 0.35
    plt.bar(sums - width/2, emp, width=width, label="Empirical")
    plt.bar(sums + width/2, th, width=width, label="Theoretical")

    plt.xlabel("Sum")
    plt.ylabel("Probability")
    plt.title("Two Dice: Monte Carlo vs Analytical Probabilities")
    plt.xticks(sums)
    plt.legend()
    plt.savefig(out_path, dpi=150)
    plt.close()
    return out_path
