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

Open `http://localhost:5000/` in a browser for a small demo interface with colors and sound. The slot machine now supports **Mini**, **Minor**, and **Mega** jackpots.

API endpoints:

- `POST /spin/<machine>` – spins the specified slot machine, spending tokens. Returns JSON with win status, jackpot name if any, payout amount, and current balance.
- `GET /balance/<user>` – retrieves the user's token balance.
- `POST /deposit/<user>` – add tokens to the user's account.

The project is at an early stage and will be expanded with additional games, Stripe integration, and a more robust token system.
