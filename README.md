# Marvels Casino

This repository contains a work-in-progress prototype for a Marvel-themed virtual casino. It currently provides a minimal Flask server with a basic slot machine implementation and a simple token economy.

## Requirements

- Python 3.8+
- `pip install -r requirements.txt`

## Usage

Run the development server:

```bash
python -m marvels_casino.server
```

Open `http://localhost:5000/` in a browser for a small demo interface with colors and sound. The slot machine now supports **Mini**, **Minor**, and **Mega** jackpots. The demo also includes a scratchoff ticket and prize wheel that award tokens. As you spend tokens, you earn VIP points and collect bonus tokens when reaching new VIP levels.

API endpoints:

- `POST /spin/<machine>` – spins the specified slot machine, spending tokens. Returns JSON with win status, jackpot name if any, payout amount, bonus tokens from VIP progress, current balance and VIP level.
- `GET /balance/<user>` – retrieves the user's token balance.
- `POST /deposit/<user>` – add tokens to the user's account.
- `POST /crypto/deposit/<user>` – deposit cryptocurrency and receive tokens.
- `POST /crypto/withdraw/<user>` – redeem tokens for cryptocurrency payout.
- `POST /scratchoff/<user>` – play a scratchoff ticket.
- `POST /wheel/<user>` – spin the prize wheel.
- `GET /vip/<user>` – retrieve the user's VIP level and points.

The project is at an early stage and will be expanded with additional games, Stripe integration, cryptocurrency payments, and a more robust token system. Crypto withdrawals are simulated and reported as processing instantly, completing within five minutes in a real deployment.
