from ui.pageobjects.basepage import BasePage
from ui.pageobjects.decorators import capture_screenshot_on_failure


class Notifications(BasePage):
    """Stranka s notifikacemi"""

    notification_list = "//ul[@data-test='notifications-list']"
    notification_item = "//ul[@data-test='notifications-list']"\
        "//span[contains(@class,'MuiTypography-displayBlock') and contains(text(),'{user} {action}')]/../.."
    notification_text_field = "//li[@data-test='{data_test_id}']/div/span"
    notification_dismiss_button = "//li[@data-test='{data_test_id}']/button"

    @capture_screenshot_on_failure
    def wait_for_notification_list(self):
        """Ceka na nacteni seznamu notifikaci"""
        self.logger.console('  ..cekam na nacteni seznamu upozorneni')
        self.selib.wait_until_page_contains_element(self.notification_list, 15)

    @capture_screenshot_on_failure
    def click_notification_dismiss_button(self, user="", action=""):
        """Stiskne tlacitko `DISMISS` pro upozoreni obsahujici daneho uzivatele a danou akci

        :param user: uzivatel (jmeno a prijmeni), ktereho se tyka upozorneni ktere ma byt smazano
        :param action: akce, ktere se tyka upozorneni, ktere ma byt smazano
        Oba vstupni parametry mohou byt prazdne retezce, v tom pripade bude smazano prvni upozorneni
        """
        notification_item = self.notification_item.format(user=user, action=action)
        notification_item_list = self.selib.get_webelements(notification_item)
        if len(notification_item_list) == 0:
            return 'None'
        data_test_id = self.selib.get_element_attribute(notification_item_list[0], "data-test")
        notification_text_field = self.notification_text_field.format(data_test_id=data_test_id)
        notification_text = self.selib.get_text(notification_text_field)
        notification_dismiss_button = self.notification_dismiss_button.format(data_test_id=data_test_id)
        self._wait_and_click_element(notification_dismiss_button)
        return notification_text
