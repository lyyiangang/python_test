import math

class Node:
    def __init__(self, point, left=None, right=None):
        self.point = point
        self.left = left
        self.right = right

def build_kdtree(points, depth=0):
    if not points:
        return None
    
    k = len(points[0])  # Number of dimensions
    axis = depth % k
    sorted_points = sorted(points, key=lambda x: x[axis])
    median = len(sorted_points) // 2

    return Node(
        point=sorted_points[median],
        left=build_kdtree(sorted_points[:median], depth + 1),
        right=build_kdtree(sorted_points[median + 1:], depth + 1)
    )

def euclidean_distance(point1, point2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(point1, point2)))

def points_within_radius(tree, target, radius, depth=0, points_within=None):
    if tree is None:
        return points_within
    
    k = len(target)
    axis = depth % k

    distance = euclidean_distance(target, tree.point)

    if distance <= radius:
        if points_within is None:
            points_within = []
        points_within.append(tree.point)

    if tree.point[axis] - target[axis] <= radius:
        points_within = points_within_radius(tree.right, target, radius, depth + 1, points_within)
    if target[axis] - tree.point[axis] <= radius:
        points_within = points_within_radius(tree.left, target, radius, depth + 1, points_within)

    return points_within

if __name__ == "__main__":
    # Example usage
    points = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
    target_point = (6, 3)
    radius = 2

    kd_tree = build_kdtree(points)
    points_within_radius = points_within_radius(kd_tree, target_point, radius)

    print(f"Points: {points}")
    print(f"Target Point: {target_point}")
    print(f"Points within Radius: {points_within_radius}")
