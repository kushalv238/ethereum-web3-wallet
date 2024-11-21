from flask import Flask, request, jsonify,send_file
from io import BytesIO
from flask_cors import CORS
from web3 import Web3
import qrcode
import re

import config

app = Flask(__name__)

# CORS(app, resources={r"/*": {"origins": "http://192.168.29.25:5500"}},
#      supports_credentials=True,
#      methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
#      allow_headers=["Content-Type", "Authorization"])

# Enable CORS for all origins
CORS(app)

# Connect to Ethereum network using Infura
web3 = Web3(Web3.HTTPProvider(config.INFURA_URL))

# Check connection status
if not web3.is_connected():
    print("Failed to connect to Ethereum network.")
else:
    print("Connected to Ethereum network.")

# Route to get the balance from the Ethereum address
@app.route('/balance', methods=['GET'])
def get_balance():
    """Retrieve balance from the Ethereum address."""
    address = config.MY_ADDRESS
    try:
        balance_wei = web3.eth.get_balance(address)
        balance_eth = web3.from_wei(balance_wei, 'ether')
        return jsonify({'address': address, 'balance': balance_eth})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Function to validate Ethereum address
def is_valid_eth_address(address):
    return re.match(r"^0x[a-fA-F0-9]{40}$", address)

@app.route('/history', methods=['GET'])
def get_transaction_history():
    """Retrieve transaction history for an Ethereum address."""
    address = request.args.get('address', config.MY_ADDRESS)
    
    try:
        # Get the latest block number
        latest_block = web3.eth.block_number
        
        # Fetch logs from the blockchain
        # This gets transactions involving the provided address
        logs = []
        for block_number in range(latest_block, latest_block - 5, -1):  # Fetch the last 5 blocks
            block = web3.eth.get_block(block_number, full_transactions=True)
            for tx in block['transactions']:
                if tx['from'] == address or tx['to'] == address:
                    logs.append(tx)

        if logs:
            return jsonify({'address': address, 'transactions': logs})
        else:
            return jsonify({'error': 'No transactions found for this address'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Route to estimate gas fee
@app.route('/gas-fee', methods=['GET'])
def estimate_gas_fee():
    """Estimate gas fee for a transaction."""
    try:
        gas_price = web3.eth.gas_price
        return jsonify({'gas_price': web3.from_wei(gas_price, 'gwei')})
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

@app.route('/qr-code', methods=['GET'])
def generate_qr_code():
    """Generate a QR code for an Ethereum address."""
    address = config.MY_ADDRESS
    try:
        img = qrcode.make(address)
        buf = BytesIO()
        img.save(buf)
        buf.seek(0)
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
