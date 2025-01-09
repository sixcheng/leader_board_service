class Player:
    def __init__(self, player_id, score, timestamp):
        self.player_id = player_id
        self.score = score
        self.timestamp = timestamp
        self.skip_list_score = self.score

    def __repr__(self):
        return f"Player(id={self.player_id}, score={self.score}, timestamp={self.timestamp})"
