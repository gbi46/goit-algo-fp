import uuid
import os
from collections import deque

import networkx as nx
import matplotlib.pyplot as plt
import imageio.v2 as imageio


# =========================
# Node & Tree Construction
# =========================

class Node:
    """
    Binary tree node.
    Keeps: value, left, right, a display color (overridden during traversal),
    and a unique id (useful for NetworkX nodes).
    """
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def build_tree_from_level_array(level_list, color_fn=None):
    """
    Build a binary tree from a level-order (heap-like) array.
    None in the array means "no node" at that index.

    Args:
        level_list: list of values (e.g., [1, 3, 5, 7, 9, 11, 13])
        color_fn: optional function (value, index) -> initial color (str)

    Returns:
        root: Node
    """
    if not level_list:
        return None

    # Create nodes or None placeholders
    nodes = []
    for i, v in enumerate(level_list):
        if v is None:
            nodes.append(None)
        else:
            color = color_fn(v, i) if color_fn else "skyblue"
            nodes.append(Node(v, color=color))

    # Connect children using array indices
    n = len(nodes)
    for i in range(n):
        if nodes[i] is None:
            continue
        li = 2 * i + 1
        ri = 2 * i + 2
        if li < n and nodes[li] is not None:
            nodes[i].left = nodes[li]
        if ri < n and nodes[ri] is not None:
            nodes[i].right = nodes[ri]

    return nodes[0]


# ======================================
# Graph & Positions (ITERATIVE; no recursion)
# ======================================

def build_graph_and_positions_iter(root):
    """
    Build a NetworkX DiGraph and a positions dict iteratively.

    Positioning rule (same geometry as in your Task 4):
        - Root at (0, 0)
        - For a node at (x, y) and depth 'layer':
            left  -> (x - 1 / 2^layer, y - 1)
            right -> (x + 1 / 2^layer, y - 1)

    Returns:
        G: nx.DiGraph with node attributes {'label', 'color'}
        pos: dict node_id -> (x, y)
    """
    if root is None:
        raise ValueError("Empty tree")

    G = nx.DiGraph()
    pos = {root.id: (0.0, 0.0)}

    # Add root
    G.add_node(root.id, color=root.color, label=root.val)

    # BFS over structure to compute positions iteratively
    q = deque([(root, 0.0, 0.0, 1)])  # (node, x, y, layer)
    while q:
        node, x, y, layer = q.popleft()

        # Left child
        if node.left:
            lx = x - 1 / (2 ** layer)
            ly = y - 1
            pos[node.left.id] = (lx, ly)
            G.add_node(node.left.id, color=node.left.color, label=node.left.val)
            G.add_edge(node.id, node.left.id)
            q.append((node.left, lx, ly, layer + 1))

        # Right child
        if node.right:
            rx = x + 1 / (2 ** layer)
            ry = y - 1
            pos[node.right.id] = (rx, ry)
            G.add_node(node.right.id, color=node.right.color, label=node.right.val)
            G.add_edge(node.id, node.right.id)
            q.append((node.right, rx, ry, layer + 1))

    return G, pos


# =========================
# Iterative Traversals
# =========================

def dfs_preorder_iter(root):
    """
    Preorder DFS (Root -> Left -> Right) using an explicit STACK.
    Returns list of Node in visit order.
    """
    if not root:
        return []
    order = []
    stack = [root]
    while stack:
        node = stack.pop()
        order.append(node)
        # push right first so left is processed first
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return order


def bfs_level_order_iter(root):
    """
    Level-order BFS using a QUEUE.
    Returns list of Node in visit order.
    """
    if not root:
        return []
    order = []
    q = deque([root])
    while q:
        node = q.popleft()
        order.append(node)
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)
    return order


# =========================
# Color Utilities (HEX)
# =========================

def _hex_from_rgb(rgb):
    r, g, b = rgb
    return "#{:02X}{:02X}{:02X}".format(
        max(0, min(255, int(r))),
        max(0, min(255, int(g))),
        max(0, min(255, int(b))),
    )


def _lerp(a, b, t):
    return a + (b - a) * t


def gradient_hex(start_hex, end_hex, n):
    """
    Make n HEX colors from dark -> light.
    Args:
        start_hex: e.g., "#10223A"
        end_hex:   e.g., "#9FD3FB"
        n: number of colors
    """
    def to_rgb(h):
        h = h.lstrip("#")
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    if n <= 0:
        return []
    s = to_rgb(start_hex)
    e = to_rgb(end_hex)
    if n == 1:
        return [_hex_from_rgb(s)]

    out = []
    for i in range(n):
        t = i / (n - 1)
        rgb = (_lerp(s[0], e[0], t), _lerp(s[1], e[1], t), _lerp(s[2], e[2], t))
        out.append(_hex_from_rgb(rgb))
    return out


# =========================
# Drawing & Animation
# =========================

def _draw_frame(G, pos, id_to_color, title, filename):
    """
    Render a single frame:
      - visited nodes colored with id_to_color
      - unvisited nodes shown in light gray
    """
    plt.close('all')
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    try:
        fig.canvas.manager.set_window_title(title)
    except Exception:
        pass

    # Node colors (visited get their assigned color; others are gray)
    colors = []
    labels = {}
    for nid, data in G.nodes(data=True):
        labels[nid] = data.get("label", "")
        colors.append(id_to_color.get(nid, "#D3D3D3"))

    nx.draw(
        G,
        pos=pos,
        labels=labels,
        arrows=False,
        node_size=2500,
        node_color=colors
    )
    ax.set_title(title)
    ax.set_axis_off()
    
    fig.savefig(filename, dpi=140, bbox_inches="tight")
    plt.close(fig)


def make_traversal_gif(root, traversal_nodes, dark_hex, light_hex, out_path, title_prefix, frame_duration=0.7):
    """
    Build a GIF visualizing traversal step-by-step.
    Each visited node receives a unique HEX color from a dark->light gradient.

    Args:
        root: tree root (Node)
        traversal_nodes: list[Node] in visit order
        dark_hex, light_hex: gradient endpoints
        out_path: output GIF file path
        title_prefix: figure title prefix
        frame_duration: seconds per frame in GIF
    """
    G, pos = build_graph_and_positions_iter(root)

    # build color palette by visit index
    palette = gradient_hex(dark_hex, light_hex, len(traversal_nodes))
    id_to_color = {}  # node id -> assigned hex

    # temp frames directory
    tmp_dir = os.path.join(os.path.dirname(out_path) or ".", "frames")
    os.makedirs(tmp_dir, exist_ok=True)
    frame_paths = []

    # initial frame (no nodes visited)
    f0 = os.path.join(tmp_dir, f"{os.path.basename(out_path)}_frame_000.png")
    _draw_frame(G, pos, id_to_color, f"{title_prefix} (step 0)", f0)
    frame_paths.append(f0)

    # incremental frames after each visit
    for i, node in enumerate(traversal_nodes, start=1):
        id_to_color[node.id] = palette[i - 1]
        fi = os.path.join(tmp_dir, f"{os.path.basename(out_path)}_frame_{i:03d}.png")
        _draw_frame(G, pos, id_to_color, f"{title_prefix} (step {i})", fi)
        frame_paths.append(fi)

    # combine into GIF
    with imageio.get_writer(out_path, mode='I', duration=frame_duration) as writer:
        for p in frame_paths:
            writer.append_data(imageio.imread(p))
