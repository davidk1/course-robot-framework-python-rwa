from PageObjectLibrary import PageObject




class BasePage(PageObject):
    """Trida pro praci s page objects"""

    def _wait_for_element(self, locator, timeout=None, error_message=None):
        """Po zadanou dobu ceka zda stranka obsahuje element, je viditelny a aktivni.

        :param locator: selector pozadovaneho elementu na strance
        :param timeout: pocet vterin po ktery se bude na element cekat, defaultni hodnota je 5 vterin
        :param error_message: chybova hlaska v pripade chyby
        """
        self.selib.wait_until_page_contains_element(locator, timeout, error_message)
        self.selib.wait_until_element_is_visible(locator, timeout)
        self.selib.wait_until_element_is_enabled(locator, timeout)

    def _wait_and_click_element(self, locator, timeout=None, error_message=None):
        """Pocka na element pomoci _wait_for_element a nasledne na nej klikne.

        :param locator: selector pozadovaneho elementu na strance
        :param timeout: pocet vterin po ktery se bude na element cekat, defaultni hodnota je 5 vterin
        :param error_message: chybova hlaska v pripade chyby
        """
        self._wait_for_element(locator, timeout, error_message)
        self.selib.click_element(locator)

    def _wait_for_element_and_type_text(self, locator, text, timeout=None, error_message=None):
        """Pocka na element pomoci _wait_for_element, klikne na na nej a vlozi text pomoci press keys.

        :param locator: selector pozadovaneho elementu na strance
        :param text: text, ktery chceme do elementu vlozit
        :param timeout: pocet vterin po ktery se bude na element cekat, defaultni hodnota je 5 vterin
        :param error_message: chybova hlaska v pripade chyby
        """
        self._wait_and_click_element(locator, timeout, error_message)
        self.selib.wait_until_element_is_enabled(locator, timeout)
        self.selib.press_keys(None, text)
