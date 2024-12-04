from flask import Flask, request, jsonify,send_file
from io import BytesIO
from flask_cors import CORS
from web3 import Web3
import qrcode
import re
import requests

import config

app = Flask(__name__)

# CORS(app, resources={r"/*": {"origins": "http://192.168.29.25:5500"}},
#      supports_credentials=True,
#      methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
#      allow_headers=["Content-Type", "Authorization"])

# Enable CORS for all origins
CORS(app)

# Etherscan API Base URL
ETHERSCAN_BASE_URL = "https://api-sepolia.etherscan.io/api"

# Function to validate Ethereum address
def is_valid_eth_address(address):
    return re.match(r"^0x[a-fA-F0-9]{40}$", address)

@app.route('/balance', methods=['GET'])
def get_balance():
    """Retrieve balance from the Ethereum address using Etherscan."""
    address = config.MY_ADDRESS
    try:
        url = ETHERSCAN_BASE_URL
        params = {
            'module': 'account',
            'action': 'balance',
            'address': address,
            'tag': 'latest',
            'apikey': config.ETHERSCAN_API_KEY
        }
        response = requests.get(url, params=params)
        data = response.json()
        if data['status'] == "1":
            balance_wei = int(data['result'])
            balance_eth = balance_wei / 10**18  # Convert Wei to Ether
            return jsonify({'address': address, 'balance': balance_eth})
        else:
            raise Exception(data['message'])
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/tx', methods=['GET'])
def get_transaction():
    """Retrieve transaction details using Etherscan."""
    tx_hash = request.args.get('tx_hash')
    try:
        url = ETHERSCAN_BASE_URL
        params = {
            'module': 'proxy',
            'action': 'eth_getTransactionByHash',
            'txhash': tx_hash,
            'apikey': config.ETHERSCAN_API_KEY
        }
        response = requests.get(url, params=params)
        data = response.json()
        if 'result' in data and data['result']:
            tx = data['result']
            if(tx["blockNumber"] is None):
                raise Exception("Transaction is processing")
            return jsonify({
                "blockNumber": int(tx["blockNumber"], 16),
                "from": tx["from"],
                "to": tx["to"],
                "value": int(tx["value"], 16) / 10**18,  # Convert Wei to Ether
                "hash": tx["hash"]
            })
        else:
            raise Exception("Transaction not found")
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/history', methods=['GET'])
def get_transaction_history():
    """Retrieve transaction history using Etherscan."""
    address = request.args.get('address', config.MY_ADDRESS)

    try:
        # Ensure the address is checksummed
        if not is_valid_eth_address(address):
            raise Exception("Invalid Ethereum address")
        
        url = ETHERSCAN_BASE_URL
        params = {
            'module': 'account',
            'action': 'txlist',
            'address': address,
            'startblock': 0,
            'endblock': 99999999,
            'page': 1,
            'offset': 100,
            'sort': 'asc',
            'apikey': config.ETHERSCAN_API_KEY,
        }

        response = requests.get(url, params=params)
        data = response.json()
        
        if data['status'] == "1":
            transactions = data['result']
            return jsonify({'address': address, 'transactions': transactions})
        else:
            raise Exception(data['message'])

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/gas-fee', methods=['GET'])
def estimate_gas_fee():
    """Retrieve current gas price using Etherscan."""
    try:
        url = ETHERSCAN_BASE_URL
        params = {
            'module': 'proxy',
            'action': 'eth_gasPrice',
            'apikey': config.ETHERSCAN_API_KEY
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'result' in data:
            gas_price_wei = int(data['result'], 16)
            gas_price_gwei = gas_price_wei / 10**9  # Convert Wei to Gwei
            return jsonify({'gas_price': gas_price_gwei})
        else:
            raise Exception("Unable to fetch gas price")
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/send', methods=['POST'])
def send_transaction():
    """Send Ether to a specified address."""
    # Connect to Ethereum network using Infura
    web3 = Web3(Web3.HTTPProvider(config.INFURA_URL))

    # Check connection status
    if not web3.is_connected():
        print("Failed to connect to Ethereum network.")
    else:
        print("Connected to Ethereum network.")

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
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(config.MY_ADDRESS),
        }

        # Sign the transaction
        signed_tx = web3.eth.account.sign_transaction(transaction, private_key=config.MY_PRIVATE_KEY)

        # Send the transaction
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(tx_hash)
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
