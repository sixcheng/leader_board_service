import time

from skip_list import SkipList
from player import Player


class LeaderBoardService:
    def __init__(self):
        self.skiplist = SkipList(max_level=4, probability=0.5)

    # 更新玩家分数
    def update_score(self, player_id, score, timestamp):
        # 查找是否已经存在该玩家，如果存在，则更新分数
        player_node = self.skiplist.search(player_id)
        if player_node:
            player_node.player.score = score
            player_node.player.timestamp = timestamp
            # 重新调整位置
            self.skiplist.delete(player_id)
            self.skiplist.insert(player_node.player)
        else:
            # 如果不存在，则插入新的玩家
            player = Player(player_id, score, timestamp)
            self.skiplist.insert(player)

    # 获取玩家当前排名
    def get_player_rank(self, player_id):
        current = self.skiplist.header.forward[0]
        rank = 1

        while current:
            if current.player.player_id == player_id:
                return rank
            current = current.forward[0]
            rank += 1

        return None

    # 获取排行榜前N名
    def get_top_n(self, n):
        current = self.skiplist.header.forward[0]
        top_n = []

        while current and len(top_n) < n:
            top_n.append(current.player)
            current = current.forward[0]

        return top_n

    # 获取玩家周边排名
    def get_player_rank_range(self, player_id, rank_range):
        current = self.skiplist.header.forward[0]
        rank = 1
        result = []

        # 查找玩家所在的排名，并记录该玩家和其周围的玩家
        while current:
            if current.player.player_id == player_id:
                # 添加玩家本身
                result.append(current.player)
                # 向前查找排名范围
                temp_rank = rank - 1
                prev = current.forward[0]  # 向后遍历
                while temp_rank > 0 and prev:
                    result.insert(0, prev.player)  # 插入到最前
                    prev = prev.forward[0]
                    temp_rank -= 1

                # 向后查找排名范围
                temp_rank = rank + 1
                next_node = current.forward[0]  # 向后遍历
                while temp_rank <= rank_range + rank:
                    if next_node:
                        result.append(next_node.player)
                        next_node = next_node.forward[0]
                        temp_rank += 1
                    else:
                        break
                return result

            rank += 1
            current = current.forward[0]

        return []


if __name__ == "__main__":
    leaderboard = LeaderBoardService()

    # 插入一些玩家数据
    leaderboard.update_score(1, 100, time.time())
    leaderboard.update_score(2, 200, time.time())
    leaderboard.update_score(3, 150, time.time())
    leaderboard.update_score(4, 50, time.time())
    leaderboard.update_score(5, 120, time.time())
    leaderboard.update_score(6, 200, time.time())

    # 打印前3名
    print("前3名玩家:")
    top_3 = leaderboard.get_top_n(3)
    for player in top_3:
        print(player)

    # 获取玩家排名
    print(f"玩家2的排名: {leaderboard.get_player_rank(2)}")

    # 获取玩家周边排名
    print(f"玩家3的周边排名范围(2名): {leaderboard.get_player_rank_range(3, 2)}")

    # 更新玩家分数并查看变动
    leaderboard.update_score(3, 250, time.time())
    print(f"玩家3更新后的排名: {leaderboard.get_player_rank(3)}")

    # 打印所有玩家的排名
    print("所有玩家的排名:")
    leaderboard.skiplist.print_list()
