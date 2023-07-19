// g++ -o ./build/dbscan dbscan.cpp --std=c++11 && ./build/dbscan

#include <iostream>
#include <vector>
#include <cmath>
// #include "kdtree.hpp"
#include <memory>

struct Point {
    double x, y;

    Point(double x = 0, double y = 0) : x(x), y(y) {}
};

double euclideanDistance(const Point& p1, const Point& p2) {
    double dx = p1.x - p2.x;
    double dy = p1.y - p2.y;
    return std::sqrt(dx * dx + dy * dy);
}


class DBScan{
    public:
        DBScan(const std::vector<Point>& points);
        std::vector<int> run(double epsilon, int minPoints);
        std::vector<int> regionQuery(const std::vector<Point>& points, int pointIdx, double epsilon);
        void expandCluster(const std::vector<Point>& points, int pointIdx, int clusterId, std::vector<int>& cluster, double epsilon, int minPoints);
        std::vector<int> getCluster()const;

    private:
        std::vector<int> m_clusters;
        std::vector<Point> m_points;
        // std::unique_ptr<KDTree> m_kdtree;//use kdtree to boost.
};