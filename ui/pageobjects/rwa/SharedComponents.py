
from ui.pageobjects.BasePage import BasePage
from ui.pageobjects.BasePage import capture_screenshot_on_failure


class SharedComponents(BasePage):
    """Sdilene komponenty pro vsechny stranky aplikace"""

    new_transaction_button = "css:a[data-test=nav-top-new-transaction]"
    logout_button = "css:div[data-test=sidenav-signout]"
    menu_item_notifications = "css:a[data-test=sidenav-notifications]"
    account_balance_label = "css:h6[data-test=sidenav-user-balance]"

    @capture_screenshot_on_failure
    def click_new_transaction_button(self):
        """Stiskne tlacitko `$ NEW` pro otevreni nove transakce"""
        self.wait_and_click_element(self.new_transaction_button)

    @capture_screenshot_on_failure
    def click_logout_button(self):
        """Stiskne tlacitko `Logout` pro odhlaseni z aplikace"""
        self.wait_and_click_element(self.logout_button)

    @capture_screenshot_on_failure
    def click_menu_notifications(self):
        """Stiskne nabidku `Notifications` v nabudce menu"""
        self. wait_and_click_element(self.menu_item_notifications)

    @capture_screenshot_on_failure
    def get_account_balance(self):
        """Nacte aktualni zustatek na uctu

        :returns accnout_balance: aktualni zustatek na uctu
        """
        account_balance = self.selib.get_text(self.account_balance_label)
        account_balance = account_balance.lstrip('$')
        return account_balance
