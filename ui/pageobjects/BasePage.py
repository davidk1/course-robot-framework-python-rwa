import functools
from PageObjectLibrary import PageObject


class BasePage(PageObject):
    """ High level class for page objects """

    def wait_for_element(self, element, timeout=None, error_message=None):
        """
        Po zadanou dobu ceka zda stranka obsahuje element, je viditelny a zapnuty.
        :param element: selector pozadovaneho elementu na strance
        :param timeout: pocet vterin po ktery se bude na element cekat, defaultni hodnota je 5 vterin
        :param error_message: chybova hlaska v pripade chyby
        :return: None
        """
        self.selib.wait_until_page_contains_element(element, timeout, error_message)
        self.selib.wait_until_element_is_visible(element, timeout)
        self.selib.wait_until_element_is_enabled(element, timeout)

    def wait_and_click_element(self, selector, timeout=None):
        """
        Pocka na element, nez pomoci wait for element funkce a nasledne na nej klikne.
        :param selector: selector pozadovaneho elementu na strance
        :param timeout: pocet vterin po ktery se bude na element cekat, defaultni hodnota je 5 vterin
        :return: None
        """
        self.wait_for_element(selector, timeout)
        self.selib.click_element(selector)

    def wait_for_element_and_type_text(self, selector, text, timeout=None):
        """
        Pocka na element pomoci wait for element funkce, klikne na na nej a vlozi text.
        :param selector: selector pozadovaneho elementu na strance
        :param text: text, ktery chceme do elementu vlozit
        :param timeout: pocet vterin po ktery se bude na element cekat, defaultni hodnota je 5 vterin
        :return: None
        """
        self.wait_and_click_element(selector, timeout)
        self.selib.press_keys(None, text)


def capture_screenshot_on_failure(func):
    """
    Decorator, ktery v pripade chyby ulozi fotku obrazovky a do chybove zpravy prida URI aktuaalni stranky aplikace.
    priklad pouziti:
        @capture_screenshot_on_failure
        def my_functioon():
            ...
    :param func: volana funkce
    :return: odpoved volane funkce
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            response = func(self, *args, **kwargs)
            return response
        except Exception as exc:
            self.selib.capture_page_screenshot()
            url = self.selib.get_location()
            raise type(exc)(str(exc) + "\n" + "URI stranky aplikace: " + url)
    return wrapper
