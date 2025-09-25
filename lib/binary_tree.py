import uuid
import networkx as nx
import matplotlib.pyplot as plt


class Node:
    """
    Node class for a binary tree.
    Each node has: value, left child, right child, color, and unique id.
    """
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())  # unique identifier for each node


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    """
    Recursive helper to add nodes and edges into a networkx graph.
    - graph: directed graph
    - node: current node
    - pos: dictionary of coordinates for visualization
    - x, y: position of current node
    - layer: tree depth (used to calculate x spacing)
    """
    if node is not None:
        # add current node with its attributes
        graph.add_node(node.id, color=node.color, label=node.val)

        # process left child
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer  # move left
            pos[node.left.id] = (l, y - 1)  # lower y = deeper level
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)

        # process right child
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer  # move right
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)

    return graph


def draw_tree(tree_root, title="Binary Heap"):
    """
    Draws the tree using matplotlib and networkx.
    """
    plt.close('all')
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}  # root at (0,0)
    tree = add_edges(tree, tree_root, pos)

    # extract colors and labels
    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}

    fig = plt.figure(num=title, figsize=(8, 5))

    try:
        fig.canvas.manager.set_window_title(title)
    except Exception:
        pass
    
    nx.draw(tree, pos=pos, labels=labels, arrows=False,
            node_size=2500, node_color=colors)
    plt.title(title)
    plt.axis('off')
    plt.show()


def build_tree_from_level_array(level_list, color_fn=None):
    """
    Build a binary tree from a level-order array (heap representation).
    None means "no node" at that position.
    color_fn: optional function to assign colors per node (value, index).
    """
    if not level_list:
        return None

    # create Node objects
    nodes = []
    for i, v in enumerate(level_list):
        if v is None:
            nodes.append(None)
        else:
            color = color_fn(v, i) if color_fn else "skyblue"
            nodes.append(Node(v, color=color))

    # connect children using array indices
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

    return nodes[0]  # return root


def visualize_heap(heap_array, color_fn=None, title="Binary Heap"):
    """
    Visualize a binary heap given as an array.
    """
    root = build_tree_from_level_array(heap_array, color_fn=color_fn)
    if root is None:
        raise ValueError("Heap is empty. Nothing to visualize.")
    draw_tree(root, title=title)
