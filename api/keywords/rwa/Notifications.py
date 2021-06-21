import _common.libraries.factory.concretefactory as concretefactory


class Notifications:
    """Klicova slova pro praci s notifikacemi."""

    def __init__(self):
        self.factory = concretefactory.ConcreteFactory()
        self.api = self.factory.create_http_requests
        self.builtin = self.factory.create_robot_builtin
        self.drq = self.factory.create_data_for_request
        self.dataprovider = self.factory.get_dataprovider
        self.logging = self.factory.get_logging

        self.notif_dict = None
