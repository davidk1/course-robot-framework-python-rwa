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
    def get_notifications_list(self):
        """KW vraci python slovnik se vsemi notifikacemi prihlaseneho uzivatele pomoci GET /notification."""
        # prepare-test-data
        request_method = self.drq.get_request_method('${TD_GET_NOTIFS_LIST}')
        request_url = self.drq.get_request_url('${API_NAME}', '${TD_GET_NOTIFS_LIST}' )
        #send request (poslat dotaz): vrati vsechny notifikace uzivatele

        resp = self.api.send_request(request_method, request_url)
        resp_json = resp.json()
        self.logging.warning(f'uzivatel ma:{len(resp_json["results"])} notifikaci')


