# TechFin Trading API Documentation

## Client Module

### Class: Client

The `Client` class manages trading operations for individual clients.

#### Methods:

- `__init__(code: str, password: str, capital: float) -> None`
  - Initializes a new trading client
  - Parameters:
    - `code`: Client identification code
    - `password`: Client password
    - `capital`: Trading capital amount
  - Raises: `TradingError` if initialization fails

- `get_quantity(price: float) -> int`
  - Calculates trading quantity based on capital and price
  - Parameters:
    - `price`: Current price of the instrument
  - Returns: Calculated quantity as integer
  - Raises: `ValueError` if price is invalid

- `get_holding_quantity(symbol: str) -> int`
  - Gets quantity of a symbol in holdings
  - Parameters:
    - `symbol`: Trading symbol
  - Returns: Quantity held as integer

- `refresh_session() -> bool`
  - Refreshes the trading session
  - Returns: `True` if successful, `False` otherwise

## Token Data Module

### Class: TokenData

The `TokenData` class handles token information retrieval and caching.

#### Methods:

- `get_token_info(symbol: str, exch_seg: str = 'NSE', instrumenttype: str = 'OPTIDX', strike_price: float = 0, pe_ce: str = '') -> pd.DataFrame`
  - Gets token information based on parameters
  - Parameters:
    - `symbol`: Trading symbol
    - `exch_seg`: Exchange segment ('NSE' or 'NFO')
    - `instrumenttype`: Instrument type ('OPTIDX', 'FUTSTK', etc.)
    - `strike_price`: Strike price for options
    - `pe_ce`: PE/CE indicator for options
  - Returns: DataFrame with token information
  - Raises: `TokenDataError` if data retrieval fails

- `get_symbols() -> List[str]`
  - Gets list of available symbols
  - Returns: Sorted list of symbol names

- `get_instrument_types() -> List[str]`
  - Gets list of available instrument types
  - Returns: Sorted list of instrument types

## UI Components

### Class: ValidatedLineEdit

Custom QLineEdit with validation support.

#### Methods:

- `__init__(placeholder: str, validator: Optional[Callable[[str], bool]] = None, parent: Optional[QtWidgets.QWidget] = None)`
  - Parameters:
    - `placeholder`: Placeholder text
    - `validator`: Optional validation function
    - `parent`: Parent widget

### Class: NumericLineEdit

Line edit for numeric input with validation.

#### Methods:

- `__init__(placeholder: str, allow_float: bool = True, min_value: Optional[float] = None, max_value: Optional[float] = None, parent: Optional[QtWidgets.QWidget] = None)`
  - Parameters:
    - `placeholder`: Placeholder text
    - `allow_float`: Whether to allow floating-point numbers
    - `min_value`: Minimum allowed value
    - `max_value`: Maximum allowed value
    - `parent`: Parent widget

### Class: SymbolLineEdit

Line edit for trading symbols with validation.

#### Methods:

- `__init__(placeholder: str = "Enter Symbol", parent: Optional[QtWidgets.QWidget] = None)`
  - Parameters:
    - `placeholder`: Placeholder text
    - `parent`: Parent widget

## Configuration

### Class: Config

Application configuration management.

#### Settings:

- `API_KEY`: SmartAPI key from environment variables
- `SYMBOLS`: List of supported trading symbols
- `ORDER_TYPES`: List of supported order types
- `OPTION_TYPES`: List of supported option types
- `SEGMENT_TYPES`: List of supported segment types
- `DEBUG`: Debug mode flag
- `LOG_LEVEL`: Logging level

#### Methods:

- `setup_directories()`: Creates necessary directories
- `get_encryption_key()`: Gets or generates encryption key
- `encrypt_credentials(client_code: str, password: str) -> tuple`: Encrypts client credentials
- `decrypt_credentials(encrypted_code: str, encrypted_pass: str) -> tuple`: Decrypts client credentials 