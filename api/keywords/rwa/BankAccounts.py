import logging
from deepdiff import DeepDiff
from robot.libraries.BuiltIn import BuiltIn
from _common.libraries.dataprovider import dataprovider
from _common.libraries.requests.api_requests import send_request


class BankAccounts:
    """Klicova slova pro praci s bankovnimi ucty."""

    def __init__(self):
        self.builtin = BuiltIn()
        self.session = self.builtin.get_variable_value('${SESSION_ID}')

    def check_bank_account(self):
        """KW overi detaily vychoziho bankovniho uctu prihlaseneho uzivatele."""

        service_method = 'get'
        service_name = 'bankAccounts'
        service_url = dataprovider.get_api_url(self.builtin.get_variable_value('${API_NAME}'), service_name)
        # send-request: ziska detail vsech bankovnich uctu prihlaseneho uzivatele pomoci GET /bankAccounts
        resp = send_request(self.session, service_method, service_url)
        resp_json = resp.json()
        # check: kontrola slovniku v odpovedi z api vuci ocekavanemu slovniku z testovacich dat
        expected_resp = dataprovider.get_var(self.builtin.get_variable_value('${CHECK_BANK_ACC}'), 'expected_response')
        diff = DeepDiff(resp_json, expected_resp)
        assert diff == {}, f'Chyba v detailu bankovniho uctu vraceneho z api: {diff}'
        logging.warning(f'check-resp-dict: detaily uctu z api jsou ok')
