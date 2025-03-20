import pytest
from unittest.mock import Mock, patch
from models.client import Client, TradingError

@pytest.fixture
def mock_smart_connect():
    with patch('models.client.SmartConnect') as mock:
        mock_instance = Mock()
        mock_instance.generateSession.return_value = {
            'data': {'refreshToken': 'test_token'}
        }
        mock_instance.getProfile.return_value = {'name': 'Test User'}
        mock_instance.holding.return_value = {'data': []}
        mock_instance.position.return_value = {'data': []}
        mock.return_value = mock_instance
        yield mock

@pytest.fixture
def test_client(mock_smart_connect):
    return Client('test_code', 'test_pass', 100000.0)

def test_client_initialization(test_client):
    """Test successful client initialization."""
    assert test_client.code == 'test_code'
    assert test_client.password == 'test_pass'
    assert test_client.capital == 100000.0
    assert test_client.obj is not None
    assert test_client.data is not None
    assert test_client.profile is not None

def test_client_initialization_failure(mock_smart_connect):
    """Test client initialization failure."""
    mock_smart_connect.return_value.generateSession.return_value = {}
    
    with pytest.raises(TradingError):
        Client('test_code', 'test_pass', 100000.0)

def test_get_quantity(test_client):
    """Test quantity calculation."""
    assert test_client.get_quantity(100.0) == 100
    assert test_client.get_quantity(50.0) == 200
    
    with pytest.raises(ValueError):
        test_client.get_quantity(0)
    
    with pytest.raises(ValueError):
        test_client.get_quantity(-100)

def test_get_holding_quantity(test_client):
    """Test getting holding quantity."""
    # Test with no holdings
    assert test_client.get_holding_quantity('TEST') == 0
    
    # Test with holdings
    test_client.holdings = {
        'data': [
            {'tradingsymbol': 'TEST', 'quantity': 100},
            {'tradingsymbol': 'OTHER', 'quantity': 50}
        ]
    }
    assert test_client.get_holding_quantity('TEST') == 100
    assert test_client.get_holding_quantity('OTHER') == 50
    assert test_client.get_holding_quantity('NONEXISTENT') == 0

def test_refresh_session(test_client, mock_smart_connect):
    """Test session refresh."""
    # Test successful refresh
    assert test_client.refresh_session() is True
    
    # Test failed refresh
    mock_smart_connect.return_value.generateSession.side_effect = Exception('API Error')
    assert test_client.refresh_session() is False

def test_update_positions_and_holdings(test_client, mock_smart_connect):
    """Test updating positions and holdings."""
    # Test successful update
    test_client._update_positions_and_holdings()
    assert test_client.holdings is not None
    assert test_client.positions is not None
    
    # Test failed update
    mock_smart_connect.return_value.holding.side_effect = Exception('API Error')
    with pytest.raises(TradingError):
        test_client._update_positions_and_holdings() 