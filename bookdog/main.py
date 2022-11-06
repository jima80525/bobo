# -*- coding: utf-8 -*-
# bookdog/main.py

"""This module provides bookdog application."""

import sys

from PyQt5.QtWidgets import QApplication

from .database import createConnection
from .views import Window

def main():
    """Bookdog main function."""
    app = QApplication(sys.argv)
    if not createConnection("books.sqlite"):
        sys.exit(1)
    win = Window()
    win.show()
    sys.exit(app.exec())
