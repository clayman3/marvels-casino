import random

class PrizeWheel:
    """Wheel of prizes with token payouts."""

    def __init__(self, cost: int = 1, segments=None):
        self.cost = cost
        self.segments = segments or [0, 2, 5, 10, 20]

    def spin(self) -> int:
        return random.choice(self.segments)
