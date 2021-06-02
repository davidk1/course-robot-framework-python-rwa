import _common.libraries.factory.concretefactory as concretefactory


class UserDetail:
    """Klicova slova pro praci s detaily prihlaseneho uzivatele."""

    def __init__(self):
        self.factory = concretefactory.ConcreteFactory()
        self.api = self.factory.create_http_requests
        self.builtin = self.factory.create_robot_builtin
        self.dfr = self.factory.create_data_for_request
        self.dataprovider = self.factory.get_dataprovider
        self.logging = self.factory.get_logging

    def get_user_detail(self, key):
        """Metoda vraci vybrany detail o prihlasenem uzivateli zavolanim GET /checkAuth.

        :param key: klic v python slovniku, ke kteremu se, v odpovedi z GET /checkAuth, vyhleda odpovidajici hodnota
        """
        # prepare-test-data
        request_method = self.dfr.get_request_method('${TD_GET_USER_DETAIL}')
        request_url = self.dfr.get_request_url('${API_NAME}', '${TD_GET_USER_DETAIL}')
        # send-request: z api GET /checkAuth ziska detail prihlaseneho uzivatele
        resp = self.api.send_request(request_method, request_url)
        resp_json = resp.json()
        user_detail = resp_json['user'][key]
        self.logging.warning(f'get-user-detail: pozadovany detail uzivatele pro klic: {key} je hodnota: {user_detail}')
        return user_detail
