# Ethereum Wallet App with Flask and Web3

This project is a simple Ethereum wallet application that allows users to check the balance of any Ethereum address and send transactions using Flask and Web3 and a frontend built with HTML, CSS, and JavaScript.

## Setup

1. Clone the repository and navigate to the project directory.
```bash
git clone https://github.com/kushalv238/ethereum-web3-wallet && cd ethereum-web3-wallet
```

2. (Optional) Create a virtual environment and activate it.
```bash
python -m venv venv && .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Replace values in [`config.py`](backend/config.py) with your Ethereum details.

## Running the App

1. Start the Flask server:
```bash
cd backend && python app.py
```

2. Navigate to the frontend directory and open the frontend file

## Usage

### 1. Get Balance
Retrieve balance for your specified Ethereum address.
```bash
curl http://127.0.0.1:5000/balance
```

### 2. Send Transaction
Send Ether to another address.
```bash
curl -X POST -H "Content-Type: application/json" -d '{"to": "RECEIVER_ETH_ADDRESS", "amount": 0.01}' http://127.0.0.1:5000/send
```
replace `RECEIVER_ETH_ADDRESS` with receivers ethereum address

### 3. View Transaction History
Retrieve the last 5 transactions involving for your Ethereum address.

```bash
curl http://127.0.0.1:5000/history
```
### 4. Estimate Gas Fee
Retrieve the current gas price for transactions on the Ethereum network.

```bash
curl http://127.0.0.1:5000/gas-fee
```

### 5. Generate QR Code
Generate a QR code for a specified Ethereum address.

```bash
curl http://127.0.0.1:5000/qr-code
```

## Notes
Ensure you’re using a test network like Sepolia for testing, as real transactions incur real costs.


---

### Important Security Note

This example is for educational purposes and should not be used as-is in a production environment. Exposing your private key is risky. For real-world applications, store private keys securely using environment variables or a dedicated secure vault.