from typing import Dict, List, Tuple

Item = Dict[str, Dict[str, int]]

def greedy_algorithm(items: Item, budget: int) -> Tuple[List[str], int, int]:
    """
    Greedy algorithm:
    Sort food items by calories-to-cost ratio (descending).
    Pick items while staying within the budget.
    Returns: (chosen_items, total_cost, total_calories).
    """
    # Sort items by ratio calories/cost, then by calories, then by cheaper cost
    order = sorted(
        items.items(),
        key=lambda kv: (kv[1]["calories"] / kv[1]["cost"], kv[1]["calories"], -kv[1]["cost"]),
        reverse=True,
    )

    chosen, total_cost, total_cal = [], 0, 0
    for name, info in order:
        if total_cost + info["cost"] <= budget:
            chosen.append(name)
            total_cost += info["cost"]
            total_cal += info["calories"]
    return chosen, total_cost, total_cal


def dynamic_programming(items: Item, budget: int) -> Tuple[List[str], int, int]:
    """
    Dynamic Programming approach (0/1 Knapsack):
    dp[i][b] = maximum calories achievable
               considering first i items with budget b.
    We also keep a 'take' table to reconstruct which items were chosen.
    Returns: (chosen_items, total_cost, total_calories).
    """
    names = list(items.keys())
    n = len(names)
    costs = [items[name]["cost"] for name in names]
    cals  = [items[name]["calories"] for name in names]

    # Initialize DP table (n+1) x (budget+1)
    dp = [[0] * (budget + 1) for _ in range(n + 1)]
    take = [[False] * (budget + 1) for _ in range(n + 1)]

    # Fill DP table
    for i in range(1, n + 1):
        cost_i, cal_i = costs[i - 1], cals[i - 1]
        for b in range(budget + 1):
            # Option 1: don't take item i
            dp[i][b] = dp[i - 1][b]
            # Option 2: take item i (if budget allows)
            if cost_i <= b and dp[i - 1][b - cost_i] + cal_i > dp[i][b]:
                dp[i][b] = dp[i - 1][b - cost_i] + cal_i
                take[i][b] = True

    # Reconstruct chosen items
    b = budget
    chosen: List[str] = []
    for i in range(n, 0, -1):
        if take[i][b]:
            chosen.append(names[i - 1])
            b -= costs[i - 1]
    chosen.reverse()

    total_cost = sum(items[name]["cost"] for name in chosen)
    total_cal  = sum(items[name]["calories"] for name in chosen)
    return chosen, total_cost, total_cal
