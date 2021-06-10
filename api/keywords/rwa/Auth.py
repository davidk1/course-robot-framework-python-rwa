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

    def login_to_rwa(self):
        """KW prihlasi vybraneho uzivatele do aplikace rwa."""
        # prepare-test-data
        request_method = self.drq.get_request_method('${TD_LOGIN_TO_RWA}')
        request_url = self.drq.get_request_url('${API_NAME}', '${TD_LOGIN_TO_RWA}')
        request_headers = self.drq.get_request_headers('${TD_LOGIN_TO_RWA}')
        request_body = self.drq.get_request_body('${TD_LOGIN_TO_RWA}')
        # send-request: prihlaseni uzivatele do aplikace rwa zavolanim /login
        resp = self.api.send_request(request_method, request_url, request_body, headers=request_headers)
        resp_json = resp.json()
        # check: overi odpoved z api vuci ocekavanym datum
        expected_response = self.dataprovider.get_var(self.builtin.get_variable_value('${TD_LOGIN_TO_RWA}'),
                                                      'expected_response')
        check = self.compare_results(resp_json, expected_response, exclude_paths={"root['user']['balance']"})
        assert check['bool'], f'err-login: z api se nevraci validni data pro /login: {check["detail"]}'
        self.logging.warning(f"login: doslo k uspesnemu prihlaseni uzivatele: {request_body['username']}")

    def logout_from_rwa(self):
        """KW odhlasi aktualne prihlaseneho uzivatele z aplikace rwa."""
        # prepare-test-data
        request_method = self.drq.get_request_method('${TD_LOGOUT_FROM_RWA}')
        request_url = self.drq.get_request_url('${API_NAME}', '${TD_LOGOUT_FROM_RWA}')
        # send-request: odhlaseni uzivatele z aplikace rwa pomoci /logout
        resp = self.api.send_request(request_method, request_url, allow_redirects=False)
        # check: overeni status kodu a cookies v odpovedi z api
        expected_status_code = self.dataprovider.get_var(self.builtin.get_variable_value('${TD_LOGOUT_FROM_RWA}'),
                                                         'status_code')
        expected_cookies = self.dataprovider.get_var(self.builtin.get_variable_value('${TD_LOGOUT_FROM_RWA}'),
                                                     'cookies')
        assert resp.status_code == expected_status_code, 'err: status code != 302'
        assert resp.cookies == expected_cookies, f'err-logout: server nevraci prazdne cookies, ale: {resp.cookies}'
        self.logging.warning(f"logout: doslo k uspesnemu odhlaseni uzivatele")
