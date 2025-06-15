class SlotMachine:
    """Represents a basic slot machine with jackpots."""

    def __init__(self, name: str, odds: float, jackpots: dict | None = None):
        self.name = name
        self.odds = odds
        # jackpots: {name: {"prob": float, "amount": int}}
        self.jackpots = jackpots or {}

    def spin(self, bet: int) -> dict:
        """Simulate a spin.

        Returns a dictionary with win status, jackpot name and payout.
        """
        import random

        payout = 0
        win = random.random() < self.odds
        if win:
            payout += bet * 2

        jackpot = None
        for name, info in self.jackpots.items():
            if random.random() < info.get("prob", 0):
                payout += info.get("amount", 0)
                jackpot = name
                break

        return {"win": win, "jackpot": jackpot, "payout": payout}
