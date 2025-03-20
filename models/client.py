from typing import Dict, Optional, Any
import math
from smartapi import SmartConnect
from config import Config
from utils.logger import app_logger, log_exception

class TradingError(Exception):
    """Base exception for trading related errors."""
    pass

class Client:
    """Client class for managing trading operations."""
    
    def __init__(self, code: str, password: str, capital: float) -> None:
        """
        Initialize a new trading client.
        
        Args:
            code: Client code
            password: Client password
            capital: Trading capital
            
        Raises:
            TradingError: If client initialization fails
        """
        self.code = code
        self.password = password
        self.capital = capital
        self.obj: Optional[SmartConnect] = None
        self.data: Optional[Dict[str, Any]] = None
        self.profile: Optional[Dict[str, Any]] = None
        self.holdings: Optional[Dict[str, Any]] = None
        self.positions: Optional[Dict[str, Any]] = None
        
        try:
            self._initialize_client()
        except Exception as e:
            log_exception(app_logger, e, "Client initialization failed")
            raise TradingError(f"Failed to initialize client: {str(e)}")
    
    def _initialize_client(self) -> None:
        """Initialize the SmartAPI client and fetch initial data."""
        try:
            self.obj = SmartConnect(api_key=Config.API_KEY)
            self.data = self.obj.generateSession(self.code, self.password)
            
            if not self.data or 'data' not in self.data:
                raise TradingError("Failed to generate session")
            
            self.profile = self.obj.getProfile(self.data['data']['refreshToken'])
            self._update_positions_and_holdings()
            
            app_logger.info(f"Successfully initialized client for {self.code}")
        except Exception as e:
            log_exception(app_logger, e, "SmartAPI initialization failed")
            raise
    
    def _update_positions_and_holdings(self) -> None:
        """Update current positions and holdings."""
        try:
            self.holdings = self.obj.holding()
            self.positions = self.obj.position()
        except Exception as e:
            log_exception(app_logger, e, "Failed to update positions/holdings")
            raise TradingError(f"Failed to update positions/holdings: {str(e)}")
    
    def get_quantity(self, price: float) -> int:
        """
        Calculate quantity based on capital and price.
        
        Args:
            price: Current price of the instrument
            
        Returns:
            int: Calculated quantity
            
        Raises:
            ValueError: If price is invalid
        """
        if price <= 0:
            raise ValueError("Price must be greater than 0")
        
        div = self.capital / 10
        quantity = div / price
        return math.floor(quantity)
    
    def get_holding_quantity(self, symbol: str) -> int:
        """
        Get quantity of a symbol in holdings.
        
        Args:
            symbol: Trading symbol
            
        Returns:
            int: Quantity held
        """
        try:
            if not self.holdings or 'data' not in self.holdings:
                return 0
            
            for holding in self.holdings['data']:
                if holding['tradingsymbol'] == symbol:
                    return holding['quantity']
            return 0
        except Exception as e:
            log_exception(app_logger, e, f"Error getting holding quantity for {symbol}")
            return 0
    
    def refresh_session(self) -> bool:
        """
        Refresh the trading session.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self._initialize_client()
            return True
        except Exception as e:
            log_exception(app_logger, e, "Session refresh failed")
            return False 