class BinanceAPIException(Exception):
    """Custom exception for Binance API errors."""
    def __init__(self, message, status_code=None, error_code=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

class NetworkException(Exception):
    """Custom exception for network/connection errors."""
    pass

class ValidationException(Exception):
    """Custom exception for input validation errors."""
    pass
