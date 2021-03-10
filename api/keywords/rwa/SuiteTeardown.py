from robot.libraries.BuiltIn import BuiltIn
from api.keywords.rwa.Auth import Auth


class SuiteTeardown:
    """Klicova slova pro teardown testovaci sady."""

    def __init__(self):
        self.auth = Auth()
        self.builtin = BuiltIn()
        self.session = self.builtin.get_variable_value('${SESSION_ID}')

    def teardown(self):
        """KW odhlasi prihlaseneho uzivatele z aplikace rwa a ukonci aktivni session."""
        self.auth.logout_from_rwa()
        self.session.close()
