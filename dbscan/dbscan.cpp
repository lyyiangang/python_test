#include <iostream>
#include <vector>
#include <cmath>
#include "dbscan.hpp"
#include <assert.h>

std::vector<int> DBScan::regionQuery(const std::vector<Point>& points, int pointIdx, double epsilon) {
    std::vector<int> neighbors;
    for (size_t i = 0; i < points.size(); ++i) {
        if (i != pointIdx && euclideanDistance(points[i], points[pointIdx]) <= epsilon) {
            neighbors.push_back(i);
        }
    }
    return neighbors;
}

void DBScan::expandCluster(const std::vector<Point>& points, int pointIdx, int clusterId, std::vector<int>& cluster, double epsilon, int minPoints) {
    std::vector<int> seeds = regionQuery(points, pointIdx, epsilon);
    if (seeds.size() < minPoints) {
        cluster[pointIdx] = -1; // Noise
        return;
    }

    cluster[pointIdx] = clusterId;
    for (size_t i = 0; i < seeds.size(); ++i) {
        int currentIdx = seeds[i];
        if (cluster[currentIdx] == 0) { // Only unclassified points can be expanded
            cluster[currentIdx] = clusterId; // 
            std::vector<int> currentNeighbors = regionQuery(points, currentIdx, epsilon);
            if (currentNeighbors.size() >= minPoints) {
                seeds.insert(seeds.end(), currentNeighbors.begin(), currentNeighbors.end());
            }
        }
    }
}

DBScan::DBScan(const std::vector<Point>& points) {
    m_points = points;
    // m_kdtree = std::make_unique<KDTree>(points);
}

std::vector<int> DBScan::run(double epsilon, int minPoints){
    int numPoints = m_points.size();
    std::vector<int> cluster(numPoints, 0); // 0 represents unclassified points
    int clusterId = 0;

    for (int i = 0; i < numPoints; ++i) {
        if (cluster[i] == 0) {
            expandCluster(m_points, i, clusterId + 1, cluster, epsilon, minPoints);
            if (cluster[i] != -1) {
                clusterId += 1;
            }
        }
    }

    m_clusters = cluster;
    return m_clusters;
}
std::vector<int> DBScan::getCluster()const{
    return m_clusters;
}

int main() {
    std::vector<Point> points = { {1, 2}, {1, 3}, {2, 2}, {8, 7}, {8, 8}, {25, 80}, {7, 8}, {2, 3}, {3, 2}, {9, 7}, {7, 7}, {8, 6} };
    double epsilon = 5;
    int minPoints = 3;
    DBScan dbscan(points);
    auto cluster_idxs = dbscan.run(epsilon, minPoints);

    std::cout << "Points: ";
    for (const auto& point : points) {
        std::cout << "(" << point.x << ", " << point.y << ") ";
    }
    std::cout << std::endl;

    std::cout << "Clusters: ";
    std::vector<int> ref{1, 1, 1, 2, 2, -1, 2, 1, 1, 2, 2, 2 };
    for (int idx=0; idx< cluster_idxs.size(); ++idx) {
        std::cout << cluster_idxs[idx] << " ";
        assert(cluster_idxs[idx] == ref[idx]);
    }
    std::cout << std::endl;
    return 0;
//     Points: (1, 2) (1, 3) (2, 2) (8, 7) (8, 8) (25, 80) (7, 8) (2, 3) (3, 2) (9, 7) (7, 7) (8, 6) 
// Clusters: 1 1 1 2 2 -1 2 1 1 2 2 2 
}
