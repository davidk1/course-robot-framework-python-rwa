import logging
from deepdiff import DeepDiff
from robot.libraries.BuiltIn import BuiltIn
from _common.libraries.dataprovider import dataprovider
from _common.libraries.requests.api_requests import send_request


class Auth:
    """Klicova slova pro prihlaseni a odhlaseni uzivatele do aplikace rwa."""

    def __init__(self):
        self.builtin = BuiltIn()
        self.session = self.builtin.get_variable_value('${SESSION_ID}')

    def login_to_rwa(self):
        """KW prihlasi vybraneho uzivatele do aplikace rwa."""

        service_method = 'post'
        service_name = 'login'
        service_url = dataprovider.get_api_url(self.builtin.get_variable_value('${API_NAME}'), service_name)
        service_body = dataprovider.get_var(self.builtin.get_variable_value('${LOGIN}'), 'body')
        # send-request: prihlaseni uzivatele do aplikace rwa zavolanim /login
        resp = send_request(self.session, service_method, service_url, service_body)
        resp_json = resp.json()
        # z odpovedi loginu z api se vyparsuje a ulozi parametr 'id' a 'balance' uzivatele pro test: Send money
        self.builtin.set_suite_variable('${USER_ID}', resp_json['user']['id'])
        self.builtin.set_suite_variable('${USER_BALANCE}', resp_json['user']['balance'])
        # check: overi odpoved na /login z api (python slovnik) vuci ocekavanym datum
        expected_response = dataprovider.get_var(self.builtin.get_variable_value('${LOGIN}'), 'expected_response')
        diff = DeepDiff(resp_json, expected_response)
        assert diff == {}, f'Nevraci se validni data ocekavana v ramci /login: {diff}'
        logging.warning(f"check-login: doslo k uspesnemu prihlaseni uzivatele: {service_body['username']}")

    def logout_from_rwa(self):
        """KW odhlasi aktualne prihlaseneho uzivatele z aplikace rwa."""

        service_method = 'post'
        service_name = 'logout'
        service_url = dataprovider.get_api_url(self.builtin.get_variable_value('${API_NAME}'), service_name)
        # send-request: odhlaseni uzivatele z aplikace rwa pomoci /logout
        resp = send_request(self.session, service_method, service_url, allow_redirects=False)
        # check: overeni status kodu a cookies v odpovedi z api
        expected_status_code = dataprovider.get_var(self.builtin.get_variable_value('${LOGOUT}'), 'status_code')
        expected_cookies = dataprovider.get_var(self.builtin.get_variable_value('${LOGOUT}'), 'cookies')
        assert resp.status_code == expected_status_code, 'Status code != 302'
        assert resp.cookies == expected_cookies, f'Server nevraci prazdne cookies: {resp.cookies}'
        logging.warning(f"check-logout: doslo k uspesnemu odhlaseni uzivatele")
