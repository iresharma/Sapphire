from json import dumps


class SapphireErrors(Exception):
    """Sapphire specific errors"""


class TemplatesNotFound(SapphireErrors):
    """File not found"""

    def __str__(self):
        return f"\033[0;31mSapphire could not find templates folder\033[0m"


class FileNotFoundError(SapphireErrors):
    """File not found"""

    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return f"\033[0;31mSapphire could not find: \033[1m templates/{self.filename} \033[0m \033[0m"


class DataNotIterable(SapphireErrors):
    """Data is not iterable"""

    def __init__(self, data, key):
        self.data = data
        self.key = key
        self.value = data[key]

    def __str__(self):
        return f"""\033[0;31m
Sapphire could not iterate over data: {self.key}(type {type(self.value)})
Given Data:
===============================================================
{dumps(self.data, indent=2)}
===============================================================
Data at {self.key}
===============================================================
{dumps(self.value, indent=2)}
===============================================================
\033[0m"""
