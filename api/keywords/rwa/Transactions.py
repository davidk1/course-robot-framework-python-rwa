import _common.libraries.factory.concretefactory as concretefactory


class Transactions:
    """Klicova slova pro praci s platbami."""

    def __init__(self):
        self.factory = concretefactory.ConcreteFactory()
        self.api = self.factory.create_http_requests
        self.builtin = self.factory.create_robot_builtin
        self.compare_results = self.factory.get_comparator
        self.dataprovider = self.factory.get_dataprovider
        self.drq = self.factory.create_data_for_request
        self.logging = self.factory.get_logging
        self.user_detail = self.factory.create_user_detail

        self.account_balance_before = None
        self.account_balance_after = None

    def send_money(self, name=None, amount=None):
        """KW odesle platbu ve vysi 'amount' dolaru prijemci 'name' zavolanim POST /transactions. Odpoved z api
        validuje vuci ocekavanym vysledkum v testovacich datech.

        :param name: existujici jmeno prijemce, kteremu se odeslou penize [str]
        :param amount: castka v [$], ktera se odesle prijemci [int]
        """
        # prepare-test-data
        name = name if name is not None else \
            self.dataprovider.get_var(self.builtin.get_variable_value('${TD_GET_RECEIVER_ID}'), 'receiver_name')
        request_method = self.drq.get_request_method('${TD_SEND_MONEY}')
        request_url = self.drq.get_request_url('${API_NAME}', '${TD_SEND_MONEY}')
        request_headers = self.drq.get_request_headers('${TD_SEND_MONEY}')
        request_body = self.drq.get_request_body('${TD_SEND_MONEY}')
        # prepare-request-body: upravi vychozi hodnoty parametru v testovacich datech
        request_body['senderId'] = self.user_detail.get_user_detail('id')  # ziskani id prihlaseneho uzivatele
        request_body['receiverId'] = self.user_detail.get_mate_detail('id', name)  # ziskani id kamarada pro odeslani $
        if amount is not None:
            request_body['amount'] = amount
        # zjisti a ulozi aktualni zustatek na uctu pred odeslanim platby
        self.account_balance_before = self._get_account_balance()
        # send-request: odesle platbu zavolanim POST /transactions
        resp = self.api.send_request(request_method, request_url, request_body, headers=request_headers)
        resp_json = resp.json()
        # zjisti a ulozi aktualni zustatek na uctu po odeslanim platby
        self.account_balance_after = self._get_account_balance()
        self.logging.warning(f'send-money: request: {request_body}')
        self.logging.warning(f'send-money: response: {resp_json}')
        self. logging.warning(f"send-money: sender-id: {request_body['senderId']}")
        self.logging.warning(f"send-money: receiver-id: {request_body['receiverId']}")
        # check: odpoved z api overi vuci parametru 'expected_response' v testovacich datech
        self._check_tx_response(request_body, resp_json)
        # check: kontrola aktualniho zustatku po odeslani platby
        self._check_account_balance(request_body['amount'])

    def _check_tx_response(self, request_body, resp_json):
        """Metoda overi vybrane parametry (detaily platby) v odpovedi (python slovniku) po odeslani platby.

        :param request_body: request body odeslany v ramci platby pomoci POST /transactions [dict]
        :param resp_json: odpoved z api po odeslani platby [dict]
        """
        # z testovacich dat nacte expected_response a nahradi parametry, ktere maji hodnotu None
        expected_resp = self.dataprovider.get_var(self.builtin.get_variable_value('${TD_SEND_MONEY}'),
                                                  'expected_response')
        expected_resp['transaction']['amount'] = request_body['amount'] * 100
        expected_resp['transaction']['receiverId'] = request_body['receiverId']
        expected_resp['transaction']['senderId'] = request_body['senderId']
        self.logging.warning(f"send-money: expected_response: {expected_resp}")
        self.logging.warning(f"send-money: actual_response: {resp_json}")
        # check: overeni vybrane parametry v odpovedi z api
        check = self.compare_results(resp_json, expected_resp,
                                     exclude_paths={"root['transaction']['id']", "root['transaction']['uuid']",
                                                    "root['transaction']['createdAt']",
                                                    "root['transaction']['modifiedAt']"})
        assert check['bool'], f'err-send-money: z api se nevraci validni data pro /transactions: {check["detail"]}'

    def _check_account_balance(self, amount=None):
        """Metoda overi, jestli doslo ke spravnemu odecteni castky po odeslani platby."""
        self.logging.warning(f'send-money: check-pred-platbou: ${self.account_balance_before/100:,}')  # zustatek pred
        expected_balance = self.account_balance_before - amount*100  # vypocitany ocekavany zustatek po odeslani platby
        self.logging.warning(f'send-money: check-po-platbe: ${expected_balance/100:,}')
        assert self.account_balance_after == expected_balance, f"err: zustatek z api {self.account_balance_after} " \
                                                               f"nesedi s ocekavanym zustatkem {expected_balance}"
        self.logging.warning(f"send-money: doslo k uspesnemu odeslani {amount} $ na ucet prijemce")

    def _get_account_balance(self):
        """Metoda vraci aktualni zustatek na uctu prihlaseneho uzivatele."""
        return self.user_detail.get_user_detail('balance')
