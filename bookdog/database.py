# -*- coding: utf-8 -*-
# rpbooks/database.py

"""This module provides a database connection."""

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

def _createBooksTable():
    """Create the books table in the database."""
    createTableQuery = QSqlQuery()
    return createTableQuery.exec(
        # NOTE: intentionally not creating a primary key at this point
        # in order to avoid having to figure out how to get it to not display
        # in the view
        """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            title VARCHAR(80) NOT NULL,
            author VARCHAR(80) NOT NULL,
            series VARCHAR(80),
            date VARCHAR(10),
            audio BOOLEAN
        )
        """
    )

def createConnection(databaseName):
    """Create and open a database connection."""
    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName(databaseName)

    if not connection.open():
        QMessageBox.warning(
            None,
            "RP Book",
            f"Database Error: {connection.lastError().text()}",
        )
        return False

    _createBooksTable()
    return True
