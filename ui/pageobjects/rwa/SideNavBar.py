from ui.pageobjects.basepage import BasePage
from ui.pageobjects.decorators import capture_screenshot_on_failure


class SideNavBar(BasePage):
    """Sdilene komponenty pro vsechny stranky aplikace"""

    logout_button = "css:[data-test=sidenav-signout]"
    menu_item_notifications = "css:[data-test=sidenav-notifications]"
    account_balance_label = "css:[data-test=sidenav-user-balance]"

    @capture_screenshot_on_failure
    def click_logout_button(self):
        """Stiskne tlacitko `Logout` pro odhlaseni z aplikace"""
        self.logger.console('  ..klikam na tlacitlo "Logout"')
        self._wait_and_click_element(self.logout_button)

    @capture_screenshot_on_failure
    def wait_for_logout_button(self):
        """Pocka na zobrazeni tlacitka Logout.

        Funkce je pouzita pro kontrolu uspesneho prihlaseni do aplikace.
        """
        self.logger.console('  ..cekam na zobrazeni tlacitka "Logout" v nabidce menu')
        self._wait_for_element(self.logout_button)

    @capture_screenshot_on_failure
    def click_menu_notifications(self):
        """Stiskne polozku `Notifications` v nabidce menu"""
        self.logger.console('  ..klikam na polozku "Notifications" v nabidce menu')
        self._wait_and_click_element(self.menu_item_notifications)

    @capture_screenshot_on_failure
    def get_account_balance(self):
        """Nacte aktualni zustatek na uctu

        :returns account_balance: aktualni zustatek na uctu
        """
        self.logger.console('  ..nacitam aktualni zuzsatek na uctu')
        self._wait_for_element(self.account_balance_label)
        account_balance = self.selib.get_text(self.account_balance_label)
        account_balance = account_balance.lstrip('$')
        return account_balance
