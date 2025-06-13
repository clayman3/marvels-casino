import random

class ScratchOff:
    """Simple scratchoff ticket game."""

    def __init__(self, cost: int = 1, odds: float = 0.1, payout: int = 5):
        self.cost = cost
        self.odds = odds
        self.payout = payout

    def play(self) -> int:
        """Returns token payout or 0."""
        return self.payout if random.random() < self.odds else 0
