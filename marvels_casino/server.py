from flask import Flask, jsonify, request, send_from_directory
from .slot_machine import SlotMachine
from .token import TokenBank

app = Flask(__name__, static_folder='static', static_url_path='')

# Simple in-memory structures
machines = {
    "fireball_frenzy": SlotMachine(
        "Fireball Frenzy",
        odds=0.2,
        jackpots={
            "mini": {"prob": 0.05, "amount": 10},
            "minor": {"prob": 0.02, "amount": 50},
            "mega": {"prob": 0.005, "amount": 500},
        },
    )
}

bank = TokenBank()

@app.route('/')
def index():
    """Serve the simple web interface."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/spin/<machine>', methods=['POST'])
def spin(machine):
    user = request.json.get('user', 'anonymous')
    cost = request.json.get('cost', 1)

    if not bank.spend_tokens(user, cost):
        return jsonify({'error': 'Insufficient tokens'}), 400

    result = machines.get(machine).spin(cost) if machine in machines else None
    if result and result['payout']:
        bank.add_tokens(user, result['payout'])

    if result is None:
        return jsonify({'error': 'Unknown machine'}), 404

    result['balance'] = bank.get_balance(user)
    return jsonify(result)

@app.route('/balance/<user>')
def balance(user):
    return jsonify({'balance': bank.get_balance(user)})

@app.route('/deposit/<user>', methods=['POST'])
def deposit(user):
    amount = request.json.get('amount', 10)
    bank.add_tokens(user, amount)
    return jsonify({'balance': bank.get_balance(user)})

if __name__ == '__main__':
    app.run(debug=True)
