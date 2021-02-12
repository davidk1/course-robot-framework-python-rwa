import os
import sys
import requests
from robot.libraries.BuiltIn import BuiltIn
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))    # nastavi root projektu
from api.keywords.rwa.Auth import Auth


class SuiteSetup:
    """Klicova slova pro setup testovaci sady."""

    def __init__(self):
        self.builtin = BuiltIn()
        self.session = requests.Session()    # vytvori jedinou session pro vsechna volani api v ramci testovaci sady
        self.builtin.set_suite_variable('${SESSION_ID}', self.session)    # ulozi aktivni session do promenne SESSION_ID
        self.auth = Auth()

    def setup(self):
        """KW prihlasi uzivatele do aplikace rwa."""
        self.auth.login_to_rwa()
