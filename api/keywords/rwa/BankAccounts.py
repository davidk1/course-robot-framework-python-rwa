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
        """KW vraci detaily uctu prihlaseneho uzivatele"""
        request_method = self.drq.get_request_method(td)
        request_url = self.drq.get_request_url('${API_NAME}', td)
        # send request
        resp = self.api.send_request(request_method, request_url)
        resp_json = resp.json()
        # check: kontrola response vs. expected response
        expected_response = self.dataprovider.get_var(self.builtin.get_variable_value(td),"expected_response")
        check = self.compare_results(resp_json, expected_response)
        assert check['bool'], f'err-login: api nevraci validni telo odpovedi pro /bankAccount: {check["detail"]}'
        self.logging.warning('get-bank-acc: detailz uctu z api jobu shodne s ocekavanymi vysledky')