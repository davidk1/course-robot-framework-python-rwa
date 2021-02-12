import os
import sys


class SetProjectRoot:
    """Nastavi cestu ke korenovemu adresari projektu."""

    def __init__(self):
        sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

    pass
