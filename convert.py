#!/usr/bin/env python3
import argparse
import json
import sys

from PyQt5.QtSql import QSqlDatabase, QSqlQuery


def get_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--infile", default="book.json", help="json file to convert"
    )
    parser.add_argument(
        "-o", "--outfile", default="test.sqlite", help="sqlite output file"
    )
    return parser.parse_args()


def read_data(database_file):
    with open(database_file, "r") as fp:
        return json.load(fp)


def _createBooksTable():
    createTableQuery = QSqlQuery()
    return createTableQuery.exec(
        """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            title VARCHAR(80) NOT NULL,
            author VARCHAR(80) NOT NULL,
            series VARCHAR(80),
            date TIMESTAMP,
            audio BOOLEAN
        )
        """
    )


def createConnection(databaseName):
    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName(str(databaseName))
    if not connection.open():
        print("NO CONNECTION")
        sys.exit(1)
    _createBooksTable()
    return connection


if __name__ == "__main__":
    args = get_command_line_args()
    db = createConnection(args.outfile)
    query = QSqlQuery()
    query.prepare(
        "INSERT into books (title, author, series, date, audio) VALUES (:title, :author, :series, :date, :audio)"
    )
    data = read_data(args.infile)
    for item in data:
        print(f"adding {item}")
        query.bindValue(":title", item["title"])
        query.bindValue(":author", item["author"])
        query.bindValue(":series", item["series"])
        query.bindValue(":date", item["date"])
        # JHA TODO at some point I should figure out the boolean goofiness
        if item["audiobook"]:
            query.bindValue(":audio", 0)
        else:
            query.bindValue(":audio", 2)

        if not query.exec_():
            print("failed query")
            sys.exit(1)
    db.commit()
