from matplotlib.patches import Polygon

import math

def draw_square(ax, x, y, size, angle, face=None, edge="#8b2b2b", lw=1.0):
    # Draw a square centered at (x, y) with given size and rotation angle
    c, s = math.cos(angle), math.sin(angle)

    # Base square points
    local = [(0, 0), (size, 0), (size, size), (0, size)]

    # Rotate and translate points
    world = [(x + u*c - v*s, y + u*s + v*c) for u, v in local]
    poly = Polygon(world, closed=True, facecolor=face or (1, 1, 1, 0), edgecolor=edge, linewidth=lw)
    ax.add_patch(poly)
    
    return world

def pythagoras_tree(ax, x, y, size, angle, depth):
    if depth < 0:
        return

    # Line width decreases with depth
    lw = max(0.5, 2.0 * (0.85 ** depth))
    p0, p1, p2, p3 = draw_square(ax, x, y, size, angle, lw=lw)

    if depth == 0:
        return
    
    # Child squares
    child = size / math.sqrt(2.0)

    # Left child
    left_angle = angle + math.pi / 4

    # p3 is the lower-left corner of the current square
    xL, yL = p3
    pythagoras_tree(ax, xL, yL, child, left_angle, depth - 1)

    # Right child
    right_angle = angle - math.pi / 4
    xR, yR = p2
    pythagoras_tree(ax, xR, yR, child, right_angle, depth - 1)
