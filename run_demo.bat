@echo off
set PY=D:\Test\Python\.venv\Scripts\python.exe
set CLI=D:\Test\TradingBot\cli.py

echo.
echo ==========================================
echo    LIVE DEMO: Binance Futures Testnet Bot
echo ==========================================
echo.

echo [STEP 1] PING TEST
%PY% %CLI% ping
echo.

echo [STEP 2] MARKET BUY ORDER - BTCUSDT - 0.002 BTC
%PY% %CLI% order --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.002
echo.

echo [STEP 3] LIMIT SELL ORDER - BTCUSDT - 0.002 BTC @ 74000
%PY% %CLI% order --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.002 --price 74000
echo.

echo ==========================================
echo    DEMO COMPLETE
echo ==========================================
