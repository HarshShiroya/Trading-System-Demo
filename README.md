# TechFin Trading Application

A professional-grade desktop trading application built with PyQt5 and SmartAPI integration. This application provides a robust platform for automated trading, with support for multiple clients, real-time market data, and advanced order management.

## Features

### Trading Capabilities
- Real-time market data monitoring
- Option chain data retrieval
- Automated order placement (Market and Limit orders)
- Position tracking and PnL monitoring
- Support for NIFTY and BANKNIFTY derivatives
- Multi-client support

### Technical Features
- Modern, responsive Qt-based UI
- Secure credential management
- Real-time data updates
- Comprehensive error handling
- Extensive logging system
- Input validation
- Automated testing

## Prerequisites

- Python 3.6+
- PyQt5
- SmartAPI
- pandas
- requests

For a complete list of dependencies, see `requirements.txt`.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/tsd.git
cd tsd
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up configuration:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Configure client credentials in `clients.csv`:
```csv
Code,Pass
your_client_code,your_password
```

## Usage

1. Start the application:
```bash
python ft.py
```

2. The application provides two main interfaces:

### Trading Interface (FMMI)
- Place market/limit orders
- Monitor positions
- Check PnL
- Real-time order status updates

### Token Information
- Retrieve token information for symbols
- Support for NIFTY and BANKNIFTY
- Options and Futures data

## Configuration

### Environment Variables
- `SMART_API_KEY`: Your SmartAPI key
- `DEBUG`: Enable debug mode (True/False)
- `LOG_LEVEL`: Logging level (INFO/DEBUG/WARNING/ERROR)

### Client Configuration
Configure trading clients in `clients.csv`:
```csv
Code,Pass
client1,password1
client2,password2
```

## Security

- API keys are stored securely in environment variables
- Client credentials are encrypted
- Input validation prevents injection attacks
- Secure session management
- Regular security updates

## Documentation

- [API Documentation](docs/API.md)
- [Development Guide](docs/DEVELOPMENT.md)
- [Change Log](CHANGELOG.md)

## Testing

Run the test suite:
```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

See [Development Guide](docs/DEVELOPMENT.md) for detailed guidelines.

## Support

For support:
1. Check the documentation
2. Search existing issues
3. Create a new issue
4. Contact the development team

## License

This project is proprietary software. All rights reserved.

## Acknowledgments

- SmartAPI team for the trading API
- PyQt team for the UI framework
- Contributors and testers

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history. 