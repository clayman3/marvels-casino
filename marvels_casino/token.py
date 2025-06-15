class TokenBank:
    """Simple token economy management."""

    def __init__(self):
        self.balances = {}

    def get_balance(self, user: str) -> int:
        return self.balances.get(user, 0)

    def add_tokens(self, user: str, amount: int) -> None:
        self.balances[user] = self.get_balance(user) + amount

    def spend_tokens(self, user: str, amount: int) -> bool:
        if self.get_balance(user) >= amount:
            self.balances[user] -= amount
            return True
        return False
