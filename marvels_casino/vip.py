class VIPManager:
    """Track VIP progress and award bonuses."""

    def __init__(self):
        # Points thresholds for levels 0..n
        self.thresholds = [0, 100, 300, 600]
        # Bonus tokens for reaching each level
        self.bonuses = {1: 5, 2: 10, 3: 20}
        self.points = {}

    def add_points(self, user: str, amount: int) -> int:
        prev_level = self.get_level(user)
        self.points[user] = self.get_points(user) + amount
        new_level = self.get_level(user)
        bonus = 0
        if new_level > prev_level:
            for lvl in range(prev_level + 1, new_level + 1):
                bonus += self.bonuses.get(lvl, 0)
        return bonus

    def get_points(self, user: str) -> int:
        return self.points.get(user, 0)

    def get_level(self, user: str) -> int:
        pts = self.get_points(user)
        level = 0
        for i, t in enumerate(self.thresholds):
            if pts >= t:
                level = i
        return level
