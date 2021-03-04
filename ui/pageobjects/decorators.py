import functools


def capture_screenshot_on_failure(func):
    """Decorator, ktery v pripade chyby ulozi fotku obrazovky a do chybove zpravy prida URI aktuaalni stranky aplikace.

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
