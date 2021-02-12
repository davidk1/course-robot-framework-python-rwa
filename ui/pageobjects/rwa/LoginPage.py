
from ui.pageobjects.BasePage import BasePage


class LoginPage(BasePage):
    """ Stranka pro prihl;aseni do aplikace """

    username_field = "username"
    password_field = "password"
    sign_in_button = "css:button[data-test=signin-submit]"

    def enter_username(self, username):
        """Vlozi text do pole `Username`.

        :param username: jmeno uzivatele
        """
        self.wait_for_element_and_type_text(self.username_field, username)

    def enter_password(self, password):
        """Vlozi zadany text do pole `Password`.

        :param password: heslo uzivatele do aplikace
        """
        self.wait_for_element_and_type_text(self.password_field, password)

    def click_sign_in_button(self):
        """Stiskne tlacitko `SIGN IN`."""
        self.wait_and_click_element(self.sign_in_button)
