// g++ -o build/kdtree kdtree.cpp --std=c++11 && ./build/kdtree
#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <ostream>
#include "kdtree.hpp"

KDTree::KDTree(std::vector<Point>& points) {
    m_root = buildKdTree(points);
}

KDTree::~KDTree(){
    dfs(m_root);
}

std::vector<Point> KDTree::findPointsWithinRadius(const Point& target, T radius) {
    std::vector<Point> result;
    pointsWithinRadius(m_root, target, radius, result);
    return result;
}

Node* KDTree::buildKdTree(std::vector<Point>& points, int depth) {
    if (points.empty()) return nullptr;

    int axis = depth % DIM;

    // Sort points and choose the median element as the pivot
    std::sort(points.begin(), points.end(), [axis](const Point& p1, const Point& p2) {
        return p1[axis] < p2[axis];
    });

    int median = points.size() / 2;
    Node* node = new Node(points[median]);

    // Recursively build the left and right subtrees
    auto left = std::vector<Point>(points.begin(), points.begin() + median);
    node->left = buildKdTree(left, depth + 1);
    auto right = std::vector<Point>(points.begin() + median + 1, points.end());
    node->right = buildKdTree(right, depth + 1);

    return node;
}

void KDTree::pointsWithinRadius(Node* node, const Point& target, T radius, std::vector<Point>& result, int depth ) {
    if (node == nullptr) return;

    int axis = depth % DIM;

    T distance = node->point.dist(target);

    if (distance <= radius) {
        result.push_back(node->point);
    }

    if (target[axis] - radius <= node->point[axis]) {
        pointsWithinRadius(node->left, target, radius, result, depth + 1);
    }

    if (target[axis] + radius >= node->point[axis]) {
        pointsWithinRadius(node->right, target, radius, result, depth + 1);
    }
}

void KDTree::dfs(Node* node){
    if(node->left)
        dfs(node->left);
    if(node->right)
        dfs(node->right);
    if(node)
        delete node;
}

int main() {
    std::vector<Point> points = { {2, 3}, {5, 4}, {9, 6}, {4, 7}, {8, 1}, {7, 2} };
    Point targetPoint(6, 3);
    T radius = 4;

    KDTree kdTree(points);
    std::vector<Point> pointsWithinRadius = kdTree.findPointsWithinRadius(targetPoint, radius);

    std::cout << "Points: ";
    for (const auto& point : points) {
        std::cout<<point;
    }
    std::cout << "Target Point: " << targetPoint;
    
    std::cout << "Points within Radius: \n";
    for (const auto& point : pointsWithinRadius) {
        std::cout<<point<<"\n";
    }
    std::cout << std::endl;

    std::cout<<"brute force method:\n";
    for(auto& pt : points){
        T dist = pt.dist(targetPoint);
        if(dist <= radius)
            std::cout<<pt<<". dist:"<<dist<<"\n";
    }
    return 0;
}
