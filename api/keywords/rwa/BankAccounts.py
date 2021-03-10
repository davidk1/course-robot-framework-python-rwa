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

    def get_bank_account(self):
        """KW overi detaily vychoziho bankovniho uctu prihlaseneho uzivatele pomoci GET /bankAccounts."""
        request_method = 'get'
        service_name = 'bankAccounts'
        request_url = dataprovider.get_api_url(self.builtin.get_variable_value('${API_NAME}'), service_name)
        # send-request: ziska detail vsech bankovnich uctu prihlaseneho uzivatele pomoci GET /bankAccounts
        resp = send_request(self.session, request_method, request_url)
        resp_json = resp.json()
        # check: kontrola python slovniku v odpovedi z api vuci ocekavanemu slovniku z testovacich dat
        self._check_bank_acc(resp_json)

    def _check_bank_acc(self, resp_json):
        """Kontrola python slovniku v odpovedi z api vuci ocekavanemu slovniku z testovacich dat.

        :param resp_json: response body vracena z api po zavolani GET /bankAccounts [python dictionary]
        """
        expected_resp = dataprovider.get_var(self.builtin.get_variable_value('${GET_BANK_ACC}'), 'expected_response')
        diff = DeepDiff(expected_resp, resp_json)
        assert diff == {}, f'err: chyba v detailu bankovniho uctu vraceneho z api: {diff}'
        logging.warning(f'get-bank-acc: detaily uctu z api jsou shodne s ocekavanymi vysledky')
