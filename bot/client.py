import time
import hmac
import hashlib
import requests
from typing import Dict, Any, Optional
from urllib.parse import urlencode

from .logging_config import logger
from .exceptions import BinanceAPIException, NetworkException

class BinanceFuturesClient:
    """Base client for interacting with Binance Futures Testnet API."""
    
    BASE_URL = "https://testnet.binancefuture.com"
    
    def __init__(self, api_key: str, api_secret: str, base_url: str = BASE_URL):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key
        })

    def _generate_signature(self, query_string: str) -> str:
        """Generate HMAC SHA256 signature."""
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def _dispatch_request(self, method: str, endpoint: str, signed: bool = False, **kwargs) -> Dict[str, Any]:
        """Internal method to send HTTP requests to the active Binance API instance."""
        url = f"{self.base_url}{endpoint}"
        
        params = kwargs.get('params', {})
        if signed:
            # Add timestamp required for signed endpoints
            params['timestamp'] = int(time.time() * 1000)
            # URL encode the parameters BEFORE generating the signature
            query_string = urlencode(params)
            signature = self._generate_signature(query_string)
            params['signature'] = signature
        
        # We rebuild the kwargs params
        kwargs['params'] = params
        
        logger.debug(f"Sending {method} request to {url} with params: {params}")
        
        try:
            response = self.session.request(method, url, **kwargs)
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error occurred: {e}")
            raise NetworkException(f"Failed to connect to Binance API: {e}") from e

        logger.debug(f"Response status: {response.status_code}")
        
        # Process the response
        try:
            data = response.json()
        except ValueError:
            data = response.text
            
        logger.debug(f"Response body: {data}")
            
        if not response.ok:
            error_msg = "Binance API Error"
            error_code = None
            if isinstance(data, dict):
                error_msg = data.get('msg', error_msg)
                error_code = data.get('code')
            
            logger.error(f"API Error {response.status_code}: [{error_code}] {error_msg}")
            raise BinanceAPIException(
                message=error_msg,
                status_code=response.status_code,
                error_code=error_code
            )
            
        return data

    def get(self, endpoint: str, signed: bool = False, **kwargs) -> Dict[str, Any]:
        return self._dispatch_request('GET', endpoint, signed, **kwargs)

    def post(self, endpoint: str, signed: bool = False, **kwargs) -> Dict[str, Any]:
        return self._dispatch_request('POST', endpoint, signed, **kwargs)

    def ping(self) -> Dict[str, Any]:
        """Test connectivity to the Rest API."""
        return self.get('/fapi/v1/ping')
