import _common.libraries.factory.concretefactory as concretefactory


class SuiteMgmt:
    """Klicova slova pro nastaveni testovaci sady (setup / teardown)."""

    def __init__(self):
        self.factory = concretefactory.ConcreteFactory()
        self.auth = self.factory.create_auth
        self.builtin = self.factory.create_robot_builtin
        self.session = self.factory.create_api_session  # vytvori instanci session pro vsechna volani rwa api v testu

    def setup(self):
        """KW prihlasi uzivatele do aplikace rwa."""
        self.builtin.set_suite_variable('${SESSION_ID}', self.session)  # ulozi instanci session do promenne SESSION_ID
        self.auth.login_to_rwa()

    def teardown(self):
        """KW odhlasi prihlaseneho uzivatele z aplikace rwa a ukonci aktivni session."""
        self.auth.logout_from_rwa()
        self.session.close()
