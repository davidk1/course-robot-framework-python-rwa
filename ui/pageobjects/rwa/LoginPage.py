from ui.pageobjects.basepage import BasePage


class LoginPage(BasePage):
    """ Stranka pro prihlaseni do aplikace """

    username_field = "username"
    password_field = "password"
    sign_in_button = "css:[data-test=signin-submit]"

    def enter_username(self, username):
        """Vlozi text do pole `Username`.

        :param username: jmeno uzivatele
        """
        self.logger.console('\tvkladam uzivatelske jmeno')
        self._wait_for_element_and_type_text(self.username_field, username)

    def enter_password(self, password):
        """Vlozi zadany text do pole `Password`.

        :param password: heslo uzivatele do aplikace
        """
        self.logger.console('\tvkladam heslo')
        self._wait_for_element_and_type_text(self.password_field, password)

    def click_sign_in_button(self):
        """Stiskne tlacitko `SIGN IN`."""
        self.logger.console('\tklikam na tlacitko "SIGN IN"')
        self._wait_and_click_element(self.sign_in_button)

    def wait_for_sign_in_button(self):
        """Pocka na zobrazeni tlacitka SIGN IN"""
        self.logger.console('\tcekam na tlacitko "SIGN IN"')
        self._wait_for_element(self.sign_in_button)
