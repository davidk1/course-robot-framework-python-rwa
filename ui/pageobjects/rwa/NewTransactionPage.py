
from ui.pageobjects.BasePage import BasePage
from ui.pageobjects.BasePage import capture_screenshot_on_failure


class NewTransactionPage(BasePage):
    """Sluzby pro prai s elementy na strance pro vytvoreni a odeslani nove transakce."""

    recipient_name_label = "//span[text()='{name}']"
    transaction_amount_field = "amount"
    transaction_description_field = "transaction-create-description-input"
    submit_transaction_button = "css:button[data-test=transaction-create-submit-payment]"

    @capture_screenshot_on_failure
    def select_recipent_by_name(self, name='Edgar Johns'):
        """Vybere prijemce platby kliknutim na jeho jmeno.

        :param name: prijemce platby
        """
        selector = self.recipient_name_label.format(name=name)
        self.wait_and_click_element(selector)

    @capture_screenshot_on_failure
    def enter_transaction_amount(self, amount=12):
        """Vyplni vysi transakce.

        :param amount: vyse transakce [int / str]
        """
        self.wait_for_element_and_type_text(self.transaction_amount_field, str(amount))

    @capture_screenshot_on_failure
    def enter_transaction_description(self, description):
        """Vyplni pole pro popis platby.

        :param description: popis platby [str]
        """
        self.wait_for_element_and_type_text(self.transaction_description_field, description)

    @capture_screenshot_on_failure
    def click_transaction_submit_button(self):
        """Stiskne tlacitko `PAY` pro odeslani platby."""
        self.wait_and_click_element(self.submit_transaction_button)
