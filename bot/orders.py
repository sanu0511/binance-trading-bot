from typing import Optional, Dict, Any
from .client import BinanceFuturesClient
from .validators import validate_order_input
from .exceptions import BinanceAPIException, NetworkException, ValidationException
from .logging_config import logger

def place_order(
    client: BinanceFuturesClient, 
    symbol: str, 
    side: str, 
    order_type: str, 
    quantity: float, 
    price: Optional[float] = None
) -> Dict[str, Any]:
    """
    Places an order on Binance Futures Testnet.
    """
    logger.info(f"Attempting to place {order_type} {side} order for {quantity} {symbol}")
    
    # 1. Validate Input
    validate_order_input(symbol, side, order_type, quantity, price)
    
    # 2. Prepare parameters
    params = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": order_type.upper(),
        "quantity": quantity,
    }
    
    if order_type.upper() == "LIMIT":
        params["price"] = price
        params["timeInForce"] = "GTC" # Good Till Cancel
        
    # 3. dispatch request
    try:
        response = client.post("/fapi/v1/order", signed=True, params=params)
        logger.info(f"Order successfully placed: OrderID={response.get('orderId')} Status={response.get('status')}")
        return response
    except BinanceAPIException as e:
        logger.error(f"Order failed due to API Error: {e.message}")
        raise
    except NetworkException as e:
        logger.error(f"Order failed due to Network Error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error occurred while placing order: {e}")
        raise
