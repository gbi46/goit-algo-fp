from colorama import Fore, init
from lib.algorithms import greedy_algorithm, dynamic_programming
from lib.binary_tree import visualize_heap
from lib.binary_tree_traversal import (
   build_tree_from_level_array, make_traversal_gif, bfs_level_order_iter, dfs_preorder_iter 
)
from lib.dijkstra import Graph, dijkstra, reconstruct_path
from lib.common import print_task_header
from lib.linked_list import LinkedList, merge_sorted_lists
from lib.monte_karlo_algo import (
    theoretical_probabilities, simulate_two_dice,
    compare_probabilities, print_table, save_plot
)
from lib.pifagor_tree import pythagoras_tree

import matplotlib.pyplot as plt
import json, math, os, time

init(autoreset=True)

def main():
    print_task_header(1)
    print(Fore.GREEN + "Linked List Operations:")
    linked_list = LinkedList()
    
    for value in [3, 1, 4, 1, 5, 9, 2, 6, 5]:
        linked_list.append(value)

    print(Fore.BLUE + "Original Linked List:")
    linked_list.print_list()

    linked_list.reverse()
    print(Fore.BLUE + "Reversed Linked List:")
    linked_list.print_list()

    linked_list.sort()
    print(Fore.BLUE + "Sorted Linked List:")
    linked_list.print_list()

    lst1 = LinkedList()
    for value in [1, 3, 5]:
        lst1.append(value)

    lst2 = LinkedList()
    for value in [2, 4, 6]:
        lst2.append(value)

    merged = merge_sorted_lists(lst1, lst2)
    print(Fore.BLUE + "Merged Linked List:")
    merged.print_list()

    time.sleep(1)
    print_task_header(2)
    print(Fore.GREEN + "Pythagoras Tree Visualization:")

    plt.ion()
    fig, ax = None, None

    while True:
        cmd = input(Fore.YELLOW + "Enter 'q' to jump to task 3 or recursion depth: ").strip().lower()

        if cmd.lower() == 'q':
            break

        if not cmd.isdigit():
            print(Fore.RED + "Please enter a valid number or 'q' to jump to task 3.")
            continue

        recursion_depth = int(cmd)
        if recursion_depth < 0:
            print(Fore.RED + "Please enter a non-negative integer.")
            continue

        if recursion_depth > 7:
            print(Fore.RED + "Recursion depth too high, please enter a value <= 7.")
            continue
        
        print(Fore.GREEN + f"Recursion depth set to: {recursion_depth}")

        if fig is None:
            fig, ax = plt.subplots(figsize=(8, 6))
            try:
                fig.canvas.manager.set_window_title("Pythagoras Tree")
            except Exception:
                pass

        ax.cla()
        ax.set_aspect('equal')
        ax.axis('off')

        pythagoras_tree(ax, x=0.0, y=1.0, size=1.0, angle=math.pi/4, depth=recursion_depth)

        ax.set_xlim(-2.2, 2.2)
        ax.set_ylim(-0.2, 3.2)

        fig.canvas.draw_idle()
        plt.pause(0.001)

    plt.ioff()
    plt.draw()

    print_task_header(3)
    print(Fore.GREEN + "Dijkstra's Algorithm for Shortest Paths:")

    # Example graph with vertices 0..5
    g = Graph(6)
    edges = [
        (0, 1, 7), (0, 2, 9), (0, 5, 14),
        (1, 2, 10), (1, 3, 15),
        (2, 3, 11), (2, 5, 2),
        (3, 4, 6),
        (4, 5, 9),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w)
        g.add_edge(v, u, w)  # make it undirected for the example

    src = 0
    dist, parent = dijkstra(g, src)

    print("Shortest distances from vertex", src, ":", dist)
    for t in range(g.n):
        path = reconstruct_path(parent, src, t)
        if path is None:
            print(f"Path {src}->{t}: unreachable")
        else:
            print(f"Path {src}->{t}: {path} (distance = {dist[t]})")

    print_task_header(4)
    print(Fore.GREEN + "Binary Heap Visualization:")

    # Example: a min-heap in array form
    heap = [1, 3, 5, 7, 9, 11, 13]

    # Optional: coloring function (different color for root and leaves)
    def demo_color_fn(value, idx):
        if idx == 0:  # root
            return "lightgreen"
        li, ri = 2 * idx + 1, 2 * idx + 2
        if li >= len(heap) and ri >= len(heap):  # leaf
            return "lightcoral"
        return "skyblue"

    # Call the visualization
    visualize_heap(heap, color_fn=demo_color_fn, title="Min-Heap Example")

    print_task_header(5)
    print(Fore.GREEN + "Binary Tree Traversal Visualization.")
    heap = [1, 3, 5, 7, 9, 11, 13]

    def demo_color_fn(value, idx):
        # Initial per-node color is irrelevant for traversal;
        # every visited node gets a dynamic color later.
        return "skyblue"

    root = build_tree_from_level_array(heap, color_fn=demo_color_fn)

    # Iterative traversals
    dfs_nodes = dfs_preorder_iter(root)       # uses STACK
    bfs_nodes = bfs_level_order_iter(root)    # uses QUEUE

    # Output files
    os.makedirs("out", exist_ok=True)
    dfs_gif = os.path.join("out", "dfs_traversal.gif")
    bfs_gif = os.path.join("out", "bfs_traversal.gif")

    # Build animations (dark -> light)
    make_traversal_gif(
        root, dfs_nodes,
        dark_hex="#10223A", light_hex="#9FD3FB",
        out_path=dfs_gif, title_prefix="DFS (stack)", frame_duration=0.7
    )
    make_traversal_gif(
        root, bfs_nodes,
        dark_hex="#2B2B2B", light_hex="#E8E8E8",
        out_path=bfs_gif, title_prefix="BFS (queue)", frame_duration=0.7
    )

    print("Saved:", dfs_gif)
    print("Saved:", bfs_gif)

    print_task_header(6)
    print(Fore.GREEN + "Demonstate greedy and dynamic algorithms")

    items = {
        "pizza": {"cost": 50, "calories": 300},
        "hamburger": {"cost": 40, "calories": 250},
        "hot-dog": {"cost": 30, "calories": 200},
        "pepsi": {"cost": 10, "calories": 100},
        "cola": {"cost": 15, "calories": 220},
        "potato": {"cost": 25, "calories": 350}
    }

    budget = 100

    g_set, g_cost, g_cal = greedy_algorithm(items, budget)
    print("Greedy:", g_set, "| cost =", g_cost, "| calories =", g_cal)

    d_set, d_cost, d_cal = dynamic_programming(items, budget)
    print("DP    :", d_set, "| cost =", d_cost, "| calories =", d_cal)

    print_task_header(7)
    print(Fore.GREEN + "Monte Carlo Simulation of Two Dice Rolls:")
    try:
        rolls = int(input("Enter number of dice rolls (default 1000000): ") or 1000000)
    except ValueError:
        print("Invalid input, using default 1000000.")
        rolls = 1000000

    theoretical = theoretical_probabilities()
    empirical, _ = simulate_two_dice(rolls)

    print_table(empirical, theoretical)

    metrics = compare_probabilities(empirical, theoretical)
    print("\nError metrics:")
    for k, v in metrics.items():
        print(f"  {k}: {v:.8f}")

    out_file = save_plot(empirical, theoretical, "probabilities.png")
    print(f"\nSaved comparison plot to: {out_file}")

    results = {
        "rolls": rolls,
        "empirical": empirical,
        "theoretical": theoretical,
        "metrics": metrics,
    }
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("Saved results to results.json")

if __name__ == "__main__":
    main()
