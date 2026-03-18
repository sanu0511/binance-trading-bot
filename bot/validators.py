from typing import Optional
from .exceptions import ValidationException

VALID_SIDES = ["BUY", "SELL"]
VALID_ORDER_TYPES = ["MARKET", "LIMIT", "STOP", "TAKE_PROFIT", "STOP_MARKET", "TAKE_PROFIT_MARKET", "TRAILING_STOP_MARKET"]

def validate_order_input(symbol: str, side: str, order_type: str, quantity: float, price: Optional[float] = None) -> None:
    """
    Validates user input before sending a request to Binance API.
    """
    if not symbol or not isinstance(symbol, str):
        raise ValidationException("Symbol must be a non-empty string (e.g., BTCUSDT).")
    
    if side.upper() not in VALID_SIDES:
        raise ValidationException(f"Invalid side '{side}'. Must be one of {VALID_SIDES}.")
        
    if order_type.upper() not in VALID_ORDER_TYPES:
        raise ValidationException(f"Invalid order_type '{order_type}'. Must be one of {VALID_ORDER_TYPES}.")

    if quantity <= 0:
        raise ValidationException("Quantity must be greater than 0.")

    if order_type.upper() == "LIMIT":
        if price is None or price <= 0:
            raise ValidationException("Price must be provided and greater than 0 for LIMIT orders.")
