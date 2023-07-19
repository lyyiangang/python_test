// g++ -o build/kdtree kdtree.cpp --std=c++11 && ./build/kdtree
#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <ostream>
#define DIM 2
using T = float;

struct Point {
    T data[DIM] = {};
    int idx = 0;
    Point(T x = 0, T y = 0, int in_idx = -1) {
        data[0] = x;
        data[1] = y;
        idx = in_idx;
    }

    T operator[](int idx){
        return data[idx];
    }

    T operator[](int idx) const{
        return data[idx];
    }

    T dist(const Point& pt){
        T sum=0;
        for(int ii = 0; ii < DIM; ++ii){
            T delta = data[ii] - pt[ii];
            sum += delta * delta;
        }
        return std::sqrt(sum);
    }

    friend std::ostream& operator <<(std::ostream& ss, const Point& pt){
        for(int idx = 0; idx < DIM; ++idx){
            ss << pt[idx]<<" ";
        }
        return ss;
    }
};

struct Node {
    Point point;
    Node* left;
    Node* right;
    Node(Point p) : point(p), left(nullptr), right(nullptr) {}
};

class KDTree {
    public:
        KDTree(const std::vector<Point>& points);

        ~KDTree();

        std::vector<Point> findPointsWithinRadius(const Point& target, T radius);

    private:
        Node* m_root;
        Node* buildKdTree(std::vector<Point>& points, int depth = 0);
        void pointsWithinRadius(Node* node, const Point& target, T radius, std::vector<Point>& result, int depth = 0);
        void dfs(Node* node);
};