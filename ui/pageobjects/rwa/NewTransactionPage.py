from ui.pageobjects.basepage import BasePage
from ui.pageobjects.decorators import capture_screenshot_on_failure


class NewTransactionPage(BasePage):
    """Metody pro praci s elementy na strance pro vytvoreni a odeslani nove transakce."""
    recipient_name_label = "//span[text()='{name}']"
    transaction_amount_field = "amount"
    transaction_note_field = "transaction-create-description-input"
    submit_transaction_button = "css:[data-test=transaction-create-submit-payment]"

    @ capture_screenshot_on_failure
    def select_recipient_by_name(self, name='Edgar Johns'):
        """Vybere prijemce platby dle jmena"""
        selector = self.recipient_name_label.format(name=name)
        self._wait_and_click_element(selector)

    @capture_screenshot_on_failure
    def enter_transaction_amount(self, amount=12):
        """Vyplni vysi transakce

        :param amount: vyse transakce [int / str]
        """
        self._wait_for_element_and_type_text(self.transaction_amount_field, str(amount))

    @capture_screenshot_on_failure
    def enter_transaction_note(self, note='poznamka'):
        """Vyplni popis platby

        :param note: popis transakce [str]
        """
        self._wait_for_element_and_type_text(self.transaction_note_field, note)

    @capture_screenshot_on_failure
    def submit_transaction(self):
        """stiskne tlacitko odeslani platby"""
        self._wait_and_click_element(self.submit_transaction_button)