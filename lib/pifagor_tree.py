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
