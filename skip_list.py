import random


# 跳跃表的节点类
class Node:
    def __init__(self, player, level):
        self.player = player  # 存储Player对象
        self.forward = [None] * (level + 1)  # 前向指针数组


# 跳跃表类
class SkipList:
    def __init__(self, max_level, probability):
        self.max_level = max_level  # 跳跃表的最大层数
        self.probability = probability  # 生成随机层数的概率
        self.header = Node(None, self.max_level)  # 跳跃表的头节点
        self.level = 0  # 当前的层数

    # 随机层数生成器
    def random_level(self):
        level = 0
        while random.random() < self.probability and level < self.max_level:
            level += 1
        return level

    # 插入节点（从大到小排序）
    def insert(self, player):
        update = [None] * (self.max_level + 1)
        current = self.header

        # 从最高层开始查找插入位置（降序）
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].player.score > player.score:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        if current and current.player.player_id == player.player_id:
            current.player = player
        else:
            new_level = self.random_level()

            # 如果新层比当前层高，则更新头节点
            if new_level > self.level:
                for i in range(self.level + 1, new_level + 1):
                    update[i] = self.header
                self.level = new_level

            # 创建新节点
            new_node = Node(player, new_level)

            # 更新前向指针
            for i in range(new_level + 1):
                new_node.forward[i] = update[i].forward[i]
                update[i].forward[i] = new_node

    # 查找节点（根据分数降序）
    def search(self, player_id):
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].player.player_id < player_id:  # 这里没有改变
                current = current.forward[i]
        current = current.forward[0]

        if current and current.player.player_id == player_id:
            return current
        return None

    # 删除节点
    def delete(self, player_id):
        update = [None] * (self.max_level + 1)
        current = self.header

        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].player.player_id < player_id:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        if current and current.player.player_id == player_id:
            # 更新前向指针
            for i in range(self.level + 1):
                if update[i].forward[i] != current:
                    break
                update[i].forward[i] = current.forward[i]

            # 如果最高层的节点已经被删除，减少层数
            while self.level > 0 and not self.header.forward[self.level]:
                self.level -= 1

    # 打印跳跃表（从大到小）
    def print_list(self):
        print("跳跃表:")
        for i in range(self.level + 1):
            current = self.header.forward[i]
            print(f"Level {i}: ", end="")
            while current:
                print(current.player, end=" -> ")
                current = current.forward[i]
            print("None")
