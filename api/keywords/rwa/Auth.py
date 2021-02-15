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
        request_method = 'post'
        service_name = 'login'
        request_url = dataprovider.get_api_url(self.builtin.get_variable_value('${API_NAME}'), service_name)
        request_body = dataprovider.get_var(self.builtin.get_variable_value('${LOGIN}'), 'body')
        # send-request: prihlaseni uzivatele do aplikace rwa zavolanim /login
        resp = send_request(self.session, request_method, request_url, request_body)
        resp_json = resp.json()
        # z odpovedi loginu z api se vyparsuje a ulozi parametr 'id' a 'balance' uzivatele pro test: Send money
        self.builtin.set_suite_variable('${USER_ID}', resp_json['user']['id'])
        self.builtin.set_suite_variable('${USER_BALANCE}', resp_json['user']['balance'])
        # check: overi odpoved z api vuci ocekavanym datum
        expected_response = dataprovider.get_var(self.builtin.get_variable_value('${LOGIN}'), 'expected_response')
        diff = DeepDiff(resp_json, expected_response, exclude_paths={"root['user']['balance']"})
        assert diff == {}, f'err: z api se nevraci validni data pro /login: {diff}'
        logging.warning(f"login: doslo k uspesnemu prihlaseni uzivatele: {request_body['username']}")

    def logout_from_rwa(self):
        """KW odhlasi aktualne prihlaseneho uzivatele z aplikace rwa."""
        request_method = 'post'
        service_name = 'logout'
        request_url = dataprovider.get_api_url(self.builtin.get_variable_value('${API_NAME}'), service_name)
        # send-request: odhlaseni uzivatele z aplikace rwa pomoci /logout
        resp = send_request(self.session, request_method, request_url, allow_redirects=False)
        # check: overeni status kodu a cookies v odpovedi z api
        expected_status_code = dataprovider.get_var(self.builtin.get_variable_value('${LOGOUT}'), 'status_code')
        expected_cookies = dataprovider.get_var(self.builtin.get_variable_value('${LOGOUT}'), 'cookies')
        assert resp.status_code == expected_status_code, 'err: status code != 302'
        assert resp.cookies == expected_cookies, f'err: server nevraci prazdne cookies, ale: {resp.cookies}'
        logging.warning(f"logout: doslo k uspesnemu odhlaseni uzivatele")
