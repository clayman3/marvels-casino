from flask import Flask, jsonify, request, send_from_directory
from .slot_machine import SlotMachine
from .token import TokenBank
from .scratchoff import ScratchOff
from .prize_wheel import PrizeWheel
from .vip import VIPManager
from .crypto import CryptoGateway

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
vip = VIPManager()
scratcher = ScratchOff()
wheel = PrizeWheel()
crypto = CryptoGateway(rate=100)  # 1 crypto unit = 100 tokens

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

    bonus = vip.add_points(user, cost)
    if bonus:
        bank.add_tokens(user, bonus)

    if result is None:
        return jsonify({'error': 'Unknown machine'}), 404

    result['balance'] = bank.get_balance(user)
    result['vip_level'] = vip.get_level(user)
    result['bonus'] = bonus
    return jsonify(result)

@app.route('/balance/<user>')
def balance(user):
    return jsonify({'balance': bank.get_balance(user)})


@app.route('/scratchoff/<user>', methods=['POST'])
def scratchoff_game(user):
    cost = request.json.get('cost', scratcher.cost)
    if not bank.spend_tokens(user, cost):
        return jsonify({'error': 'Insufficient tokens'}), 400

    payout = scratcher.play()
    if payout:
        bank.add_tokens(user, payout)

    bonus = vip.add_points(user, cost)
    if bonus:
        bank.add_tokens(user, bonus)

    return jsonify({
        'payout': payout,
        'bonus': bonus,
        'balance': bank.get_balance(user),
        'vip_level': vip.get_level(user)
    })


@app.route('/wheel/<user>', methods=['POST'])
def wheel_game(user):
    cost = request.json.get('cost', wheel.cost)
    if not bank.spend_tokens(user, cost):
        return jsonify({'error': 'Insufficient tokens'}), 400

    payout = wheel.spin()
    if payout:
        bank.add_tokens(user, payout)

    bonus = vip.add_points(user, cost)
    if bonus:
        bank.add_tokens(user, bonus)

    return jsonify({
        'payout': payout,
        'bonus': bonus,
        'balance': bank.get_balance(user),
        'vip_level': vip.get_level(user)
    })

@app.route('/deposit/<user>', methods=['POST'])
def deposit(user):
    amount = request.json.get('amount', 10)
    bank.add_tokens(user, amount)
    return jsonify({'balance': bank.get_balance(user)})


@app.route('/crypto/deposit/<user>', methods=['POST'])
def crypto_deposit(user):
    """Simulate a cryptocurrency deposit."""
    wallet = request.json.get('wallet')
    amount = request.json.get('amount', 0.0)
    tokens = crypto.process_deposit(wallet, amount)
    bank.add_tokens(user, tokens)
    return jsonify({'credited': tokens, 'balance': bank.get_balance(user)})


@app.route('/crypto/withdraw/<user>', methods=['POST'])
def crypto_withdraw(user):
    """Simulate a token payout to a crypto wallet."""
    wallet = request.json.get('wallet')
    tokens = request.json.get('amount', 0)
    if not bank.spend_tokens(user, tokens):
        return jsonify({'error': 'Insufficient tokens'}), 400
    success = crypto.send_payout(wallet, tokens)
    status = 'processing' if success else 'failed'
    return jsonify({'status': status, 'balance': bank.get_balance(user)})


@app.route('/vip/<user>')
def vip_status(user):
    return jsonify({
        'level': vip.get_level(user),
        'points': vip.get_points(user)
    })

if __name__ == '__main__':
    app.run(debug=True)
