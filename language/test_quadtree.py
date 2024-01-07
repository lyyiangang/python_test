class QuadTreeNode:
    def __init__(self, x, y, width, height):
        self.x = x  # 节点的左上角 x 坐标
        self.y = y  # 节点的左上角 y 坐标
        self.width = width  # 节点的宽度
        self.height = height  # 节点的高度
        self.points = []  # 存储在节点中的点
        self.children = []  # 子节点

    def insert(self, point):
        # 检查点是否在节点范围内
        if not self.contains_point(point):
            return False

        # 检查是否已经达到了叶子节点的最大容量
        if len(self.points) < 4 and not self.children:
            self.points.append(point)
            return True

        # 如果没有子节点，则创建四个子节点
        if not self.children:
            self.subdivide()

        # 将点插入子节点中
        for child in self.children:
            if child.insert(point):
                return True

    def subdivide(self):
        # 计算子节点的宽度和高度
        child_width = self.width / 2
        child_height = self.height / 2

        # 创建四个子节点
        self.children.append(QuadTreeNode(self.x, self.y, child_width, child_height))
        self.children.append(QuadTreeNode(self.x + child_width, self.y, child_width, child_height))
        self.children.append(QuadTreeNode(self.x, self.y + child_height, child_width, child_height))
        self.children.append(QuadTreeNode(self.x + child_width, self.y + child_height, child_width, child_height))

    def contains_point(self, point):
        return self.x <= point[0] < self.x + self.width and self.y <= point[1] < self.y + self.height

    def query_range(self, range):
        result = []

        # 检查范围是否与节点相交
        if not self.intersects_range(range):
            return result

        # 将节点中的点添加到结果中
        for point in self.points:
            if range[0][0] <= point[0] < range[1][0] and range[0][1] <= point[1] < range[1][1]:
                result.append(point)

        # 递归查询子节点
        for child in self.children:
            result.extend(child.query_range(range))

        return result

    def intersects_range(self, range):
        return not (self.x + self.width < range[0][0] or
                    self.y + self.height < range[0][1] or
                    self.x > range[1][0] or
                    self.y > range[1][1])

def test():
    # 创建根节点
    root = QuadTreeNode(0, 0, 100, 100)

    # 插入点
    root.insert((30, 40))
    root.insert((0, 20))


test()