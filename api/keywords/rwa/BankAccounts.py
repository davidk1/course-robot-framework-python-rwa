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

    def get_bank_account(self, td='${TD_GET_BANK_ACC}'):
        """Keyword overi detaily bankovniho uctu prihlaseneho uzivatele"""
        # prepare test data
        request_method = self.drq.get_request_method(td)
        request_url = self.drq.get_request_url('${API_NAME}', td)
        # send request : ziskat detail vsech bankovnich uctu prihlaseneho uzivatele
        resp = self.api.send_request(request_method,request_url)
        resp_json = resp.json()
        # check : kontrola actual vs expected bankAccount
        expected_result = self.dataprovider.get_var(self.builtin.get_variable_value(td),'expected_response')
        check = self.compare_results(resp_json, expected_result)
        assert check['bool'], f'err-get-bank-acc: chyba v detailu bankovniho uctu vraceneho z api: {check["detail"]}'
        self.logging.warning('get-bank-acc dtaily uctu z api jsou shodne s ocekavanym vysledkem')