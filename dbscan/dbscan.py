
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import DBSCAN

def dbscan(points, epsilon, min_points):
    def region_query(point_idx):
        return neighbors[point_idx]

    def expand_cluster(point_idx, cluster_id):
        cluster[point_idx] = cluster_id
        seeds = region_query(point_idx)
        for seed_idx in seeds:
            if cluster[seed_idx] == UNCLASSIFIED:
                cluster[seed_idx] = cluster_id
                if len(neighbors[seed_idx]) >= min_points:
                    seeds.append(seed_idx)

    UNCLASSIFIED = -2
    NOISE = -1
    cluster_id = 0

    num_points = len(points)
    neighbors = NearestNeighbors(n_neighbors=num_points).fit(points).kneighbors_graph(points).toarray()
    cluster = [UNCLASSIFIED] * num_points

    for point_idx in range(num_points):
        if cluster[point_idx] != UNCLASSIFIED:
            continue

        point_neighbors = region_query(point_idx)

        if len(point_neighbors) < min_points:
            cluster[point_idx] = NOISE
        else:
            cluster_id += 1
            expand_cluster(point_idx, cluster_id)

    return cluster

def test(points, epsilon, min_points):

    clusters = dbscan(points, epsilon, min_points)

    print("Points:", points)
    print("Clusters:", clusters)

if __name__ == "__main__":
    # Example usage
    points = np.array([
        [1, 2], [1, 3], [2, 2], [8, 7], [8, 8], [25, 80], [7, 8], [2, 3], [3, 2], [9, 7], [7, 7], [8, 6]
    ])

    epsilon = 5
    min_points = 3
    # test(points=points, epsilon=epsilon, min_points=min_points)
    print('using sklearn dbscan')
    cluster = DBSCAN(eps = epsilon, min_samples = min_points)
    cluster.fit(points)
    print('labels:', cluster.labels_)
    print('labels for cpp compare:', cluster.labels_ + 1)
    # -1 is noise.
    unique_labels = np.unique(cluster.labels_)
    for cur_label in unique_labels:
        if cur_label == -1:
            continue
        print(f'culster {cur_label}:{points[cluster.labels_ == cur_label]}')
