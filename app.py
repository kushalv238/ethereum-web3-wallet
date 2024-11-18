from flask import Flask, request, jsonify
from web3 import Web3
import config

app = Flask(__name__)

# Connect to Ethereum network using Infura
web3 = Web3(Web3.HTTPProvider(config.INFURA_URL))

# Check connection status
if not web3.is_connected():
    print("Failed to connect to Ethereum network.")
else:
    print("Connected to Ethereum network.")

# Route to get the balance of an Ethereum address
@app.route('/balance', methods=['GET'])
def get_balance():
    """Retrieve balance of an Ethereum address."""
    address = request.args.get('address', config.MY_ADDRESS)
    try:
        balance_wei = web3.eth.get_balance(address)
        balance_eth = web3.from_wei(balance_wei, 'ether')
        return jsonify({'address': address, 'balance': balance_eth})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Route to send Ether to a specified address
@app.route('/send', methods=['POST'])
def send_transaction():
    """Send Ether to a specified address."""
    try:
        data = request.get_json()
        to_address = data['to']
        amount_ether = data['amount']

        # Convert Ether to Wei
        amount_wei = web3.to_wei(amount_ether, 'ether')

        # Build transaction
        transaction = {
            'from': config.MY_ADDRESS,
            'to': to_address,
            'value': amount_wei,
            'gas': 21000,
            'gasPrice': web3.to_wei('20', 'gwei'),
            'nonce': web3.eth.get_transaction_count(config.MY_ADDRESS),
        }

        # Sign the transaction
        signed_tx = web3.eth.account.sign_transaction(transaction, private_key=config.MY_PRIVATE_KEY)

        # Send the transaction
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        return jsonify({'transaction_hash': tx_hash.hex()})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
