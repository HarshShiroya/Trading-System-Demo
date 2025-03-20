import requests
import pandas as pd
from datetime import datetime
from typing import Optional, Dict, List
from functools import lru_cache
from config import Config
from utils.logger import app_logger, log_exception

class TokenDataError(Exception):
    """Base exception for token data related errors."""
    pass

class TokenData:
    """Handler for token data operations."""
    
    API_URL = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
    
    def __init__(self):
        """Initialize token data handler."""
        self._df: Optional[pd.DataFrame] = None
        self._last_update: Optional[datetime] = None
        self._update_interval = pd.Timedelta(hours=24)
    
    @property
    def df(self) -> pd.DataFrame:
        """
        Get the token data DataFrame.
        
        Returns:
            pd.DataFrame: Token data
            
        Raises:
            TokenDataError: If data fetch fails
        """
        if self._should_update():
            self._update_data()
        return self._df
    
    def _should_update(self) -> bool:
        """Check if data should be updated."""
        if self._df is None or self._last_update is None:
            return True
            
        now = datetime.now()
        return (now - self._last_update) > self._update_interval
    
    def _update_data(self) -> None:
        """Update token data from API."""
        try:
            app_logger.info("Fetching token data from API...")
            response = requests.get(self.API_URL)
            response.raise_for_status()
            
            data = response.json()
            df = pd.DataFrame.from_dict(data)
            
            # Process data
            df['expiry'] = pd.to_datetime(df['expiry']).apply(lambda x: x.date())
            df = df.astype({'strike': float})
            
            self._df = df
            self._last_update = datetime.now()
            
            app_logger.info("Token data updated successfully")
        except requests.RequestException as e:
            log_exception(app_logger, e, "Failed to fetch token data")
            if self._df is None:
                raise TokenDataError(f"Failed to fetch token data: {str(e)}")
        except Exception as e:
            log_exception(app_logger, e, "Failed to process token data")
            if self._df is None:
                raise TokenDataError(f"Failed to process token data: {str(e)}")
    
    @lru_cache(maxsize=100)
    def get_token_info(
        self,
        symbol: str,
        exch_seg: str = 'NSE',
        instrumenttype: str = 'OPTIDX',
        strike_price: float = 0,
        pe_ce: str = ''
    ) -> pd.DataFrame:
        """
        Get token information based on parameters.
        
        Args:
            symbol: Trading symbol
            exch_seg: Exchange segment
            instrumenttype: Instrument type
            strike_price: Strike price
            pe_ce: PE/CE indicator
            
        Returns:
            pd.DataFrame: Filtered token information
            
        Raises:
            TokenDataError: If data retrieval fails
        """
        try:
            df = self.df
            
            if exch_seg == 'NSE':
                result = df[
                    (df['exch_seg'] == 'NSE') &
                    (df['name'] == symbol)
                ]
            elif exch_seg == 'NFO' and instrumenttype in ['FUTSTK', 'FUTIDX']:
                result = df[
                    (df['exch_seg'] == 'NFO') &
                    (df['instrumenttype'] == instrumenttype) &
                    (df['name'] == symbol)
                ].sort_values(by=['expiry'])
            elif exch_seg == 'NFO' and instrumenttype in ['OPTSTK', 'OPTIDX']:
                strike_price = strike_price * 100
                result = df[
                    (df['exch_seg'] == 'NFO') &
                    (df['instrumenttype'] == instrumenttype) &
                    (df['name'] == symbol) &
                    (df['strike'] == strike_price) &
                    (df['symbol'].str.endswith(pe_ce))
                ].sort_values(by=['expiry'])
            else:
                raise TokenDataError(f"Invalid parameters: {exch_seg}, {instrumenttype}")
            
            if len(result) == 0:
                app_logger.warning(
                    f"No data found for {symbol} ({exch_seg}, {instrumenttype})"
                )
            
            return result
        except Exception as e:
            log_exception(
                app_logger,
                e,
                f"Failed to get token info for {symbol}"
            )
            raise TokenDataError(f"Failed to get token info: {str(e)}")
    
    def get_symbols(self) -> List[str]:
        """
        Get list of available symbols.
        
        Returns:
            List[str]: Available symbols
        """
        return sorted(self.df['name'].unique().tolist())
    
    def get_instrument_types(self) -> List[str]:
        """
        Get list of available instrument types.
        
        Returns:
            List[str]: Available instrument types
        """
        return sorted(self.df['instrumenttype'].unique().tolist())

# Global instance
token_data = TokenData() 