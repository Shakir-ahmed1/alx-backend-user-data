#!/usr/bin/env python3
""" Regex-ing entries """
from typing import List
import logging
import re


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


# user_data = open('user_data.csv')
# reader = csv.reader(user_data)
# user_data.close()

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
print(get_logger.__annotations__.get('return'))
print("PII_FIELDS: {}".format(len(PII_FIELDS)))