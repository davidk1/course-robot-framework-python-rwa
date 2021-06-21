import _common.libraries.factory.concretefactory as concretefactory


class Auth:
    """Klicova slova pro prihlaseni a odhlaseni uzivatele do aplikace rwa."""

    def __init__(self):
        self.factory = concretefactory.ConcreteFactory()
        self.api = self.factory.create_http_requests
        self.builtin = self.factory.create_robot_builtin
        self.compare_results = self.factory.get_comparator
        self.drq = self.factory.create_data_for_request
        self.dataprovider = self.factory.get_dataprovider
        self.logging = self.factory.get_logging

    def login_to_rwa(self, td='${TD_LOGIN_TO_RWA}'):
        """KW prihlasi vybraneho uzivatele do aplikace rwa.

        :param td: nazev promenne obsahujici relativni cestu k testovacim datum pro login, aby bylo mozne se do aplikace
        prihlasovat pod ruznymi uzivateli; cesta k testovacim datum je zapsana pomoci teckove notace od korenu projektu
        """
        # prepare-test-data
        request_method = self.drq.get_request_method(td)
        request_url = self.drq.get_request_url('${API_NAME}', td)
        request_headers = self.drq.get_request_headers(td)
        request_body = self.drq.get_request_body(td)
        # send-request: prihlaseni uzivatele do aplikace rwa zavolanim /login
        resp = self.api.send_request(request_method, request_url, request_body, headers=request_headers)
        resp_json = resp.json()
        # check: v odpovedi z api overi telo odpovedi vuci ocekavanym vysledkum
        expected_response = self.dataprovider.get_var(self.builtin.get_variable_value(td), 'expected_response')
        check = self.compare_results(resp_json, expected_response, exclude_paths={"root['user']['balance']"})
        assert check['bool'], f'err-login: api nevraci validni telo odpovedi pro /login: {check["detail"]}'
        # check: v odpovedi z api overi existenci, neprazdnou hodnotu a spravny datovy typ cookie "connect.sid"
        self._check_session_cookie(resp)
        self.logging.warning(f"login: doslo k uspesnemu prihlaseni uzivatele: {request_body['username']}")
        self.logging.warning(f"login: session cookie connect.sid = {resp.cookies.get('connect.sid')}")

    def logout_from_rwa(self):
        """KW odhlasi aktualne prihlaseneho uzivatele z aplikace rwa."""
        # prepare-test-data
        request_method = self.drq.get_request_method('${TD_LOGOUT_FROM_RWA}')
        request_url = self.drq.get_request_url('${API_NAME}', '${TD_LOGOUT_FROM_RWA}')
        # send-request: odhlaseni uzivatele z aplikace rwa pomoci /logout
        resp = self.api.send_request(request_method, request_url, allow_redirects=False)
        # check: v odpovedi z api overi status kod a cookies vuci ocekavanym vysledkum
        expected_status_code = self.dataprovider.get_var(self.builtin.get_variable_value('${TD_LOGOUT_FROM_RWA}'),
                                                         'status_code')
        expected_cookies = self.dataprovider.get_var(self.builtin.get_variable_value('${TD_LOGOUT_FROM_RWA}'),
                                                     'cookies')
        # check: status code
        check = self.compare_results(resp.status_code, expected_status_code)
        assert check['bool'], f'err-logout: api nevraci status code {expected_status_code}, ale: {check["detail"]}'
        # check: cookies
        check = self.compare_results(resp.cookies.get_dict(), expected_cookies)
        assert check['bool'], f'err-logout: api nevraci prazdne cookies: {check["detail"]}'
        self.logging.warning('logout: doslo k uspesnemu odhlaseni uzivatele')

    def _check_session_cookie(self, resp):
        """Pomocna funkce pro kontrolu existence session cookie "connect.sid", overeni existence jeji hodnoty a
        spravneho datoveho typu.

        :param resp: python objekt - obsahuje odpoved api na odeslany http pozadavek
        """
        try:
            session_cookie = resp.cookies.get_dict()['connect.sid']    # overi existenci cookie "connect.sid"
        except KeyError:
            self.logging.error('err-login: api nevraci session cookie s nazvem "connect.sid"')
            raise
        try:
            assert session_cookie    # overi, ze cookie "connect.sid" ma nejakou hodnotu
        except AssertionError:
            self.logging.error('session cookie "connect.sid" nema zadnou hodnotu')
            raise
        try:
            assert isinstance(session_cookie, str)    # overi, ze cookie "connect.sid" ma datovy typ string
        except AssertionError:
            self.logging.error('session cookie "connect.sid" nema datovy typ "string"')
            raise
