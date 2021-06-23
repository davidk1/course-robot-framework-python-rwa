from ui.pageobjects.basepage import BasePage
from ui.pageobjects.decorators import capture_screenshot_on_failure


class TopNavBar(BasePage):
    """Sdilene komponenty pro vsechny stranky aplikace"""

    new_transaction_button = "CSS:[data-test=nav-top-new-transaction]"


    def click_new_transaction_button(self):
        """Stiskne tlacitko '$ NEW' pro otevreni nove transakce"""
        self.logger.console('  ..klikne na tlacitko "$NEW"')
        self._wait_and_click_element(self.new_transaction_button)