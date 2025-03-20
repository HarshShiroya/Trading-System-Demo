from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from typing import Optional, Callable
import re

class ValidatedLineEdit(QtWidgets.QLineEdit):
    """Line edit with validation."""
    
    def __init__(
        self,
        placeholder: str,
        validator: Optional[Callable[[str], bool]] = None,
        parent: Optional[QtWidgets.QWidget] = None
    ):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self._validator = validator
        self._is_valid = True
        self.textChanged.connect(self._validate)
        
        # Style sheets
        self.default_style = """
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
            }
        """
        self.error_style = """
            QLineEdit {
                border: 1px solid #f44336;
                border-radius: 4px;
                padding: 5px;
                background-color: #ffebee;
            }
        """
        self.setStyleSheet(self.default_style)
    
    def _validate(self):
        """Validate the current text."""
        if self._validator:
            text = self.text()
            self._is_valid = self._validator(text)
            self.setStyleSheet(
                self.default_style if self._is_valid else self.error_style
            )
    
    @property
    def is_valid(self) -> bool:
        return self._is_valid

class NumericLineEdit(ValidatedLineEdit):
    """Line edit for numeric input."""
    
    def __init__(
        self,
        placeholder: str,
        allow_float: bool = True,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        parent: Optional[QtWidgets.QWidget] = None
    ):
        def validator(text: str) -> bool:
            if not text:
                return True
            try:
                value = float(text) if allow_float else int(text)
                if min_value is not None and value < min_value:
                    return False
                if max_value is not None and value > max_value:
                    return False
                return True
            except ValueError:
                return False
        
        super().__init__(placeholder, validator, parent)

class SymbolLineEdit(ValidatedLineEdit):
    """Line edit for trading symbols."""
    
    def __init__(
        self,
        placeholder: str = "Enter Symbol",
        parent: Optional[QtWidgets.QWidget] = None
    ):
        def validator(text: str) -> bool:
            return bool(re.match(r'^[A-Z0-9]+$', text)) if text else True
        
        super().__init__(placeholder, validator, parent)

class LoadingOverlay(QtWidgets.QWidget):
    """Loading overlay with spinner."""
    
    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        # Spinner
        self.spinner = QtWidgets.QLabel()
        self.movie = QtGui.QMovie(":/images/spinner.gif")
        self.spinner.setMovie(self.movie)
        layout.addWidget(self.spinner)
        
        # Message
        self.message = QtWidgets.QLabel("Loading...")
        self.message.setStyleSheet("color: white; font-weight: bold;")
        layout.addWidget(self.message)
        
        self.hide()
    
    def showEvent(self, event):
        """Start animation when shown."""
        super().showEvent(event)
        self.movie.start()
    
    def hideEvent(self, event):
        """Stop animation when hidden."""
        super().hideEvent(event)
        self.movie.stop()
    
    def paintEvent(self, event):
        """Paint semi-transparent background."""
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtGui.QColor(0, 0, 0, 128))

class ConfirmDialog(QtWidgets.QDialog):
    """Confirmation dialog with custom styling."""
    
    def __init__(
        self,
        title: str,
        message: str,
        parent: Optional[QtWidgets.QWidget] = None
    ):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        
        layout = QtWidgets.QVBoxLayout(self)
        
        # Message
        message_label = QtWidgets.QLabel(message)
        message_label.setWordWrap(True)
        layout.addWidget(message_label)
        
        # Buttons
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 8px;
            }
            QPushButton {
                padding: 5px 15px;
                border-radius: 4px;
            }
            QPushButton[default="true"] {
                background-color: #2196f3;
                color: white;
            }
        """) 