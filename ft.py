import sys
import os
from pathlib import Path
from PyQt5 import QtWidgets
from config import Config
from models.client import Client, TradingError
from ui.components import (
    ValidatedLineEdit,
    NumericLineEdit,
    SymbolLineEdit,
    LoadingOverlay,
    ConfirmDialog
)
from utils.logger import app_logger, log_exception
import pandas as pd

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TechFin Trading")
        self.setMinimumSize(800, 600)
        
        # Initialize UI
        self._init_ui()
        
        # Load clients
        self._load_clients()
        
        # Setup loading overlay
        self.loading_overlay = LoadingOverlay(self)
        self.loading_overlay.resize(self.size())
    
    def _init_ui(self):
        """Initialize the user interface."""
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        layout = QtWidgets.QVBoxLayout(self.central_widget)
        
        # Tab widget
        self.tab_widget = QtWidgets.QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Add tabs
        self.trading_tab = self._create_trading_tab()
        self.token_tab = self._create_token_tab()
        
        self.tab_widget.addTab(self.trading_tab, "Trading")
        self.tab_widget.addTab(self.token_tab, "Token Info")
    
    def _create_trading_tab(self):
        """Create the trading interface tab."""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)
        
        # Order entry form
        form_layout = QtWidgets.QFormLayout()
        
        self.order_type = QtWidgets.QComboBox()
        self.order_type.addItems(["MARKET", "LIMIT"])
        self.order_type.currentTextChanged.connect(self._on_order_type_changed)
        
        self.symbol = SymbolLineEdit()
        self.token = NumericLineEdit("Enter Token", allow_float=False, min_value=0)
        self.quantity = NumericLineEdit("Enter Quantity", allow_float=False, min_value=1)
        self.price = NumericLineEdit("Enter Price", min_value=0)
        self.trigger_price = NumericLineEdit("Enter Trigger Price", min_value=0)
        
        form_layout.addRow("Order Type:", self.order_type)
        form_layout.addRow("Symbol:", self.symbol)
        form_layout.addRow("Token:", self.token)
        form_layout.addRow("Quantity:", self.quantity)
        form_layout.addRow("Price:", self.price)
        form_layout.addRow("Trigger Price:", self.trigger_price)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QtWidgets.QHBoxLayout()
        
        self.buy_button = QtWidgets.QPushButton("Buy")
        self.sell_button = QtWidgets.QPushButton("Sell")
        self.check_button = QtWidgets.QPushButton("Check PnL")
        
        self.buy_button.clicked.connect(self._on_buy)
        self.sell_button.clicked.connect(self._on_sell)
        self.check_button.clicked.connect(self._on_check_pnl)
        
        button_layout.addWidget(self.buy_button)
        button_layout.addWidget(self.sell_button)
        button_layout.addWidget(self.check_button)
        
        layout.addLayout(button_layout)
        
        # Status area
        self.status_text = QtWidgets.QTextBrowser()
        layout.addWidget(self.status_text)
        
        return tab
    
    def _create_token_tab(self):
        """Create the token information tab."""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)
        
        # Symbol selection
        form_layout = QtWidgets.QFormLayout()
        
        self.token_symbol = QtWidgets.QComboBox()
        self.token_symbol.addItems(Config.SYMBOLS)
        
        self.segment_type = QtWidgets.QComboBox()
        self.segment_type.addItems(Config.SEGMENT_TYPES)
        
        self.strike_price = NumericLineEdit(
            "Strike Price",
            min_value=0,
            allow_float=False
        )
        
        self.option_type = QtWidgets.QComboBox()
        self.option_type.addItems(Config.OPTION_TYPES)
        
        form_layout.addRow("Symbol:", self.token_symbol)
        form_layout.addRow("Segment:", self.segment_type)
        form_layout.addRow("Strike:", self.strike_price)
        form_layout.addRow("Option:", self.option_type)
        
        layout.addLayout(form_layout)
        
        # Submit button
        self.submit_button = QtWidgets.QPushButton("Get Token")
        self.submit_button.clicked.connect(self._on_get_token)
        layout.addWidget(self.submit_button)
        
        # Results table
        self.results_table = QtWidgets.QTableView()
        layout.addWidget(self.results_table)
        
        return tab
    
    def _load_clients(self):
        """Load client configurations."""
        try:
            self.clients_df = pd.read_csv('clients.csv')
            app_logger.info(f"Loaded {len(self.clients_df)} clients")
        except Exception as e:
            log_exception(app_logger, e, "Failed to load clients")
            self.show_error("Failed to load client configurations")
    
    def _on_order_type_changed(self, order_type):
        """Handle order type changes."""
        is_market = order_type == "MARKET"
        self.price.setEnabled(not is_market)
        self.trigger_price.setEnabled(not is_market)
    
    def _validate_order_inputs(self):
        """Validate order input fields."""
        if not all([
            self.symbol.is_valid,
            self.token.is_valid,
            self.quantity.is_valid
        ]):
            return False
        
        if self.order_type.currentText() == "LIMIT":
            if not all([
                self.price.is_valid,
                self.trigger_price.is_valid
            ]):
                return False
        
        return True
    
    def _on_buy(self):
        """Handle buy order."""
        if not self._validate_order_inputs():
            self.show_error("Please check your input values")
            return
        
        dialog = ConfirmDialog(
            "Confirm Buy Order",
            f"Place buy order for {self.quantity.text()} {self.symbol.text()}?",
            self
        )
        
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self._place_order("BUY")
    
    def _on_sell(self):
        """Handle sell order."""
        if not self._validate_order_inputs():
            self.show_error("Please check your input values")
            return
        
        dialog = ConfirmDialog(
            "Confirm Sell Order",
            f"Place sell order for {self.quantity.text()} {self.symbol.text()}?",
            self
        )
        
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self._place_order("SELL")
    
    def _place_order(self, side):
        """Place a trading order."""
        try:
            # Implementation of order placement logic
            self.show_status(f"{side} order placed successfully")
        except Exception as e:
            log_exception(app_logger, e, f"Failed to place {side} order")
            self.show_error(f"Failed to place {side} order: {str(e)}")
    
    def _on_check_pnl(self):
        """Check profit and loss."""
        try:
            # Implementation of PnL calculation
            self.show_status("PnL calculation completed")
        except Exception as e:
            log_exception(app_logger, e, "Failed to calculate PnL")
            self.show_error(f"Failed to calculate PnL: {str(e)}")
    
    def _on_get_token(self):
        """Get token information."""
        try:
            # Implementation of token information retrieval
            self.show_status("Token information retrieved")
        except Exception as e:
            log_exception(app_logger, e, "Failed to get token information")
            self.show_error(f"Failed to get token information: {str(e)}")
    
    def show_error(self, message):
        """Show error message."""
        QtWidgets.QMessageBox.critical(self, "Error", message)
    
    def show_status(self, message):
        """Show status message."""
        self.status_text.append(message)
    
    def resizeEvent(self, event):
        """Handle window resize."""
        super().resizeEvent(event)
        self.loading_overlay.resize(event.size())

def main():
    """Application entry point."""
    try:
        app = QtWidgets.QApplication(sys.argv)
        
        # Set application style
        app.setStyle("Fusion")
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        sys.exit(app.exec_())
    except Exception as e:
        log_exception(app_logger, e, "Application startup failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
