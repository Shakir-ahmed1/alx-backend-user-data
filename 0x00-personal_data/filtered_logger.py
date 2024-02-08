#!/usr/bin/env python3
""" Regex-ing entries """
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ returns the log message obfuscated """
    for field in fields:
        message = re.sub(f'{field}=[^;]*', f'{field}={redaction}',
                         message, count=0)
    return message
