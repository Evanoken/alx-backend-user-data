#!/usr/bin/env python3
""" Filtered logger module. """
import re
from typing import List
import logging
import os
from mysql.connector.connection import MySQLConnection


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class. """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Constructor method. """
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Filters values in incoming log records. """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super().format(record)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Returns the log message obfuscated. """
    for field in fields:
        message = re.sub(field + "=.*?" + separator,
                         field + "=" + redaction + separator, message)
    return message


def get_logger() -> logging.Logger:
    """ Returns a logging.Logger object. """
    # Create a logger with name 'user_data'
    logger = logging.getLogger('user_data')
    # Set the logger's level to INFO
    logger.setLevel(logging.INFO)
    # Create a stream handler with INFO level
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    # Create a formatter and set it to the stream handler
    formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler.setFormatter(formatter)
    # Add the stream handler to the logger
    logger.addHandler(stream_handler)
    # Disable propagation of other loggers
    logger.propagate = False

    return logger


def get_db() -> MySQLConnection:
    """ Returns a connector to a database. """
    user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.getenv('PERSONAL_DATA_DB_NAME')

    return MySQLConnection(user=user, password=password,
                           host=host, database=database)


def main():
    """ Main function. """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()
    for row in cursor:
        message = "name={}; email={}; phone={}; ssn={}; password={}; \
        ip={}; last_login={}; user_agent={}; ".format(row[0], row[1], row[2],
                                                      row[3], row[4], row[5],
                                                      row[6], row[7])
        logger.info(message)
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
