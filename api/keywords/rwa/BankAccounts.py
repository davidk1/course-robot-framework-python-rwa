import _common.libraries.factory.concretefactory as concretefactory


class BankAccounts:
    """Klicova slova pro praci s bankovnimi ucty."""

    def __init__(self):
        self.factory = concretefactory.ConcreteFactory()
        self.api = self.factory.create_http_requests
        self.builtin = self.factory.create_robot_builtin
        self.compare_results = self.factory.get_comparator
        self.drq = self.factory.create_data_for_request
        self.dataprovider = self.factory.get_dataprovider
        self.logging = self.factory.get_logging

    def get_bank_accounts(self, td='${TD_GET_BANK_ACC}'):
        """KW overi detaily vychoziho bankovniho uctu prihlaseneho uzivatele pomoci GET /bankAccounts.

        :param td: nazev promenne obsahujici relativni cestu k testovacim datum pro KW get bank accounts, aby bylo mozne
        ziskat detail bankovniho uctu pro ruzne uzivatele; cesta k testovacim datum je zapsana pomoci teckove notace od
        korene projektu
        """
        # prepare-test-data
        request_method = self.drq.get_request_method(td)
        request_url = self.drq.get_request_url('${API_NAME}', td)
        # send-request: ziska detail vsech bankovnich uctu prihlaseneho uzivatele pomoci GET /bankAccounts
        resp = self.api.send_request(request_method, request_url)
        resp_json = resp.json()
        # check: kontrola python slovniku v odpovedi z api vuci ocekavanemu slovniku z testovacich dat
        expected_response = self.dataprovider.get_var(self.builtin.get_variable_value(td), 'expected_response')
        check = self.compare_results(resp_json, expected_response)
        assert check['bool'], f'err-get-bank-acc: chyba v detailu bankovniho uctu vraceneho z api: {check["detail"]}'
        self.logging.warning(f'get-bank-acc: detaily uctu z api jsou shodne s ocekavanymi vysledky')
