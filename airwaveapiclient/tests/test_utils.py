# -*- coding: utf-8 -*-

"""UnitTests utils."""


def read_file(path):
    """Read file."""
    with open(path) as _file:
        return _file.read()
