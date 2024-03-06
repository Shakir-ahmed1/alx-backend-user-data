#!/usr/bin/env python3
""" Regex-ing entries """
from typing import List
import logging
import re
from mysql.connector import connect, connection
from os import environ

getenv = environ.get


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ returns the log message obfuscated """
    for field in fields:
        message = re.sub(f'{field}=[^{separator}]*', f'{field}={redaction}',
                         message, count=0)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ initialization """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ format the log """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super().format(record)


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def get_logger() -> logging.Logger:
    """ returns a logger"""
    new_log = logging.getLogger()
    new_log.propagate = False
    new_log.setLevel(logging.INFO)
    a_handler = logging.StreamHandler()
    a_formatter = RedactingFormatter(PII_FIELDS)
    a_handler.setFormatter(a_formatter)
    new_log.addHandler(a_handler)

    return new_log


def get_db() -> connection.MySQLConnection:
    """ returns a connector to a database using env variables"""
    psw = getenv("PERSONAL_DATA_DB_PASSWORD", "")
    username = getenv('PERSONAL_DATA_DB_USERNAME', "root")
    host = getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = getenv('PERSONAL_DATA_DB_NAME')
    conn = connect(
        host=host,
        database=db_name,
        user=username,
        password=psw)
    return conn


db = get_db()
cursor = db.cursor()
cursor.execute("SELECT * FROM users;")
a = get_logger()

for row in cursor:
    message = f"name={row[0]}; email={row[1]}; phone={row[2]}; " +\
              f"ssn={row[3]}; password={row[4]};ip={row[5]}; " +\
              f"last_login={row[6]}; user_agent={row[7]};"
    a.info(message)

cursor.close()
db.close()
