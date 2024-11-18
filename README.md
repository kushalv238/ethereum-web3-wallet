# Ethereum Wallet App with Flask and Web3

This project is a simple Ethereum wallet application that allows users to check the balance of any Ethereum address and send transactions using Flask and Web3.

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
4. Replace values in [`config.py`](config.py) with your Ethereum details.

## Running the App

Start the Flask server:
```bash
python app.py
```

## Usage

### 1. Get Balance
Retrieve balance for a specified Ethereum address.
```bash
curl http://127.0.0.1:5000/balance?address=YOUR_ETH_ADDRESS
```
address is optional, if no address is provided default address specified in config.py is used

### 2. Send Transaction
Send Ether to another address.
```bash
curl -X POST -H "Content-Type: application/json" -d "{\"to\": \"RECEIVER_ETH_ADDRESS\", \"amount\": 0.01}" http://127.0.0.1:5000/send
```
replace `RECEIVER_ETH_ADDRESS` with receivers ethereum address

## Notes
Ensure you’re using a test network like Sepolia for testing, as real transactions incur real costs.


---

### Important Security Note

This example is for educational purposes and should not be used as-is in a production environment. Exposing your private key is risky. For real-world applications, store private keys securely using environment variables or a dedicated secure vault.

This setup should give you a solid foundation for the implementation part of your presentation.
