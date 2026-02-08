import math

class KDNode:
    def __init__(self, point, axis, left=None, right=None):
        self.point = point   # (lat, lon, name, category)
        self.axis = axis
        self.left = left
        self.right = right


def build_kdtree(points, depth=0):
    if not points:
        return None

    k = 2
    axis = depth % k

    points.sort(key=lambda x: x[axis])
    median = len(points) // 2

    return KDNode(
        points[median],
        axis,
        build_kdtree(points[:median], depth + 1),
        build_kdtree(points[median + 1:], depth + 1)
    )


def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)


def nearest_neighbor(root, target, best=None):
    if root is None:
        return best

    axis = root.axis

    next_branch = root.left if target[axis] < root.point[axis] else root.right
    opposite_branch = root.right if target[axis] < root.point[axis] else root.left

    best = nearest_neighbor(next_branch, target, best)

    if best is None or distance(target, root.point) < distance(target, best):
        best = root.point

    if abs(target[axis] - root.point[axis]) < distance(target, best):
        best = nearest_neighbor(opposite_branch, target, best)

    return best


def range_search(root, target, radius, results):
    if root is None:
        return

    if distance(target, root.point) <= radius:
        results.append(root.point)

    axis = root.axis

    if target[axis] - radius < root.point[axis]:
        range_search(root.left, target, radius, results)

    if target[axis] + radius > root.point[axis]:
        range_search(root.right, target, radius, results)

def print_kdtree(node, prefix="", is_left=True):
    if node is None:
        return

    # Print right subtree first (goes on top)
    if node.right:
        new_prefix = prefix + ("│   " if is_left else "    ")
        print_kdtree(node.right, new_prefix, False)

    # Print current node
    connector = "└── " if is_left else "├── "
    lat, lon, name, category = node.point
    print(prefix + connector + f"({lat:.4f}, {lon:.4f}) | {name} [{category}] | axis={node.axis}")

    # Print left subtree
    if node.left:
        new_prefix = prefix + ("    " if is_left else "│   ")
        print_kdtree(node.left, new_prefix, True)

def kdtree_to_string(node, prefix="", is_left=True, lines=None):
    if lines is None:
        lines = []

    if node is None:
        return lines

    # Right child first
    if node.right:
        new_prefix = prefix + ("│   " if is_left else "    ")
        kdtree_to_string(node.right, new_prefix, False, lines)

    connector = "└── " if is_left else "├── "
    lat, lon, name, category = node.point
    lines.append(
        prefix + connector +
        f"({lat:.4f}, {lon:.4f}) | {name} [{category}] | axis={node.axis}"
    )

    # Left child
    if node.left:
        new_prefix = prefix + ("    " if is_left else "│   ")
        kdtree_to_string(node.left, new_prefix, True, lines)

    return lines