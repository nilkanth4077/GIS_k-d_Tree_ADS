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