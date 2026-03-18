# Binance Futures Testnet Trading Bot

A clean, robust, and well-structured Python trading bot wrapper for interacting directly with the Binance Futures Testnet API (USDT-M) via REST.

## Core Features
- **REST Implementation**: Built using raw Python `requests` library to demonstrate API communication and HMAC SHA256 signature generation from scratch.
- **Robust Validation**: Pre-flight checks on inputs before communicating with the Binance Testnet API.
- **Exception Handling**: Distinct custom exceptions for Network Errors, Validation Errors, and specific API Response Errors (with status and error codes mapped).
- **Beautiful CLI UX**: Powered by `Typer` and `Rich` for a colorful, informative, and engaging command-line interface.
- **Comprehensive Logging**: Automatically logs all request parameters, response payloads, and errors to `trading_bot.log`. 

## Project Structure
```text
trading_bot/
│
├── bot/
│   ├── __init__.py
│   ├── client.py          # HTTP Client & Signature Generation Layer
│   ├── exceptions.py      # Custom Exceptions Definition
│   ├── logging_config.py  # Centralized application logging
│   ├── orders.py          # Business logic: order placement orchestration
│   └── validators.py      # Pre-flight input validators
│
├── cli.py                 # The Typer command-line application
├── requirements.txt       # Project dependencies
├── .env.example           # Example environment file
└── README.md              # Documentation
```

## Setup Steps

### 1. Requirements
Ensure you have Python 3.8+ installed on your system.

### 2. Install Dependencies
Clone this repository or extract the zip archive. Navigate to the folder in your terminal and install the project requirements:
```bash
pip install -r requirements.txt
```

### 3. Setup Credentials
Copy the example environment file:
```bash
cp .env.example .env
```
Open `.env` in a text editor and paste in your Testnet API Key and Secret:
```text
API_KEY=your_testnet_api_key_here
API_SECRET=your_testnet_api_secret_here
```

## How to Run Examples

### 1. Test Connectivity
Use the `ping` command to verify that your system can reach the Binance base URL.
```bash
python cli.py ping
```

### 2. Place a MARKET Order
The following command will place a BUY order for `0.001` BTC using a MARKET configuration:
```bash
python cli.py order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### 3. Place a LIMIT Order
The following command will place a SELL limit order for `0.001` BTC at the specified price:
```bash
python cli.py order --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 90000.0
```

### 4. Viewing Application Logs
All actions via the CLI are actively logged out into an appended logfile named `trading_bot.log` in the root directory. This log captures the detailed request parameters being dispatched and raw JSON responses returned by Binance. 

## Assumptions
- The application executes in an isolated test environment using the Binance Testnet.
- Security constraints around `hmac` generation assume standard endpoint signing rules outlined in Binance API public documentation.
- Testnet liquidity isn't absolute, so very obscure limit order prices might not fill immediately; the app requests a `GTC` (Good Till Cancel) rule on Limit orders.
