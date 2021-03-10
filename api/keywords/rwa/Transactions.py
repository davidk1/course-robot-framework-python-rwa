import logging
from deepdiff import DeepDiff
from robot.libraries.BuiltIn import BuiltIn
from _common.libraries.dataprovider import dataprovider
from _common.libraries.requests.api_requests import send_request


class Transactions:
    """Klicova slova pro praci s platbami."""

    def __init__(self):
        self.builtin = BuiltIn()
        self.session = self.builtin.get_variable_value('${SESSION_ID}')
        self.receiver_id = None

    def get_receiver_id(self, name=None):
        """KW ziska z api id-cko prijemce, jemuz se odeslou penize a ulozi ho jako 'receiver_id' pro pouziti v jinych
        KW. Pokud se KW nepreda argument 'name', potom se 'receiver_id' vygeneruje na zaklade 'name' z testovacich
        dat. 'receiver_id' se ziska parsovanim odpovedi GET /users.
        """
        request_method = 'get'
        service_name = 'users'
        request_url = dataprovider.get_api_url(self.builtin.get_variable_value('${API_NAME}'), service_name)
        # send-request: z api ziska seznam pratel, vcetne vsech detailu, pomoci GET /users
        resp = send_request(self.session, request_method, request_url)
        users_list = resp.json()  # seznam pratel jako python slovnik
        # check: projde seznam pratel a podle zadaneho 'name' vrati 'receiver_id' prijemce
        receiver_id = self._get_receiver_id_from_api_resp(users_list, name)
        self.receiver_id = receiver_id
        return receiver_id

    def send_money(self, name=None, amount=None):
        """KW odesle platbu ve vysi 'amount' dolaru prijemci 'name' zavolanim POST /transactions. Odpoved z api
        validuje vuci ocekavanym vysledkum v testovacich datech.

        :param name: jmeno prijemce, kteremu se odeslou penize [str]
        :param amount: castka v [$], ktera se odesle prijemci [int]
        """
        request_method = 'post'
        service_name = 'transactions'
        request_url = dataprovider.get_api_url(self.builtin.get_variable_value('${API_NAME}'), service_name)
        request_body = dataprovider.get_var(self.builtin.get_variable_value('${SEND_MONEY}'), 'body')
        # prepare-request-body: upravi vychozi hodnoty parametru v testovacich datech
        request_body['senderId'] = self.builtin.get_variable_value('${USER_ID}')   # nacteni ${USER_ID} z KW login
        request_body['receiverId'] = self.get_receiver_id(name)
        if amount is not None:
            request_body['amount'] = amount
        # send-request: odesle platbu zavolanim POST /transactions
        resp = send_request(self.session, request_method, request_url, request_body)
        resp_json = resp.json()
        logging.warning(f'send-money: request: {request_body}')
        logging.warning(f'send-money: response: {resp_json}')
        logging.warning(f"send-money: sender-id: {request_body['senderId']}")
        logging.warning(f'send-money: receiver-id: {self.receiver_id}')
        # check: odpoved z api overi vuci parametru 'expected_response' v testovacich datech
        self._check_tx_response(request_body, resp_json)
        # check: kontrola aktualniho zustatku po odeslani platby
        self._check_current_balance(request_body['amount'])

    def _check_tx_response(self, request_body, resp_json):
        """Metoda overi vybrane parametry v python slovniku ziskane v odpovedi z api po odeslani platby vuci ocekavanym
        parametrum z testovacich dat.

        :param request_body: request body odeslany v ramci platby pomoci POST /transactions [python dictionary]
        :param resp_json: response body vracena z api po odeslani platby [python dictionary]
        """
        # nacteni template s ocekavanymi vysledky z testovacich dat a vyplneni parametru, kde je None
        expected_resp = dataprovider.get_var(self.builtin.get_variable_value('${SEND_MONEY}'), 'expected_response')
        expected_resp['transaction']['amount'] = request_body['amount'] * 100
        expected_resp['transaction']['receiverId'] = request_body['receiverId']
        expected_resp['transaction']['senderId'] = request_body['senderId']
        expected_resp['transaction']['description'] = request_body['description']
        logging.warning(f"send-money: expected_response: {expected_resp}")
        logging.warning(f"send-money: actual_response: {resp_json}")
        diff = DeepDiff(expected_resp, resp_json, exclude_paths={"root['transaction']['id']",
                                                                 "root['transaction']['uuid']",
                                                                 "root['transaction']['createdAt']",
                                                                 "root['transaction']['modifiedAt']"})
        assert diff == {}, f'err: z api se nevraci validni data pro /transactions: {diff}'

    def _check_current_balance(self, amount=None):
        """Metoda nacte aktualni zustatek uzivatele zavolanim GET /checkAuth a overi, jestli doslo ke spravnemu odecteni
        castky po odeslani platby.
        """
        request_method = 'get'
        service_name = 'checkAuth'
        request_url = dataprovider.get_api_url(self.builtin.get_variable_value('${API_NAME}'), service_name)
        # send-request: ziska detail prihlaseneho uzivatele vcetne aktualniho zustatku na uctu zavolanim GET /checkAuth
        resp = send_request(self.session, request_method, request_url)
        resp_json = resp.json()
        # check: overi konecny zustatek po odeslani platby
        resp_balance = resp_json['user']['balance']  # aktualni zustatek vraceny z api
        expected_balance = self.builtin.get_variable_value('${USER_BALANCE}')    # zustatek nacteny v ramci loginu
        logging.warning(f'send-money: check-pred-platbou: ${expected_balance/100:,}')  # zustatek pred odeslanim platby
        expected_balance = expected_balance - amount*100  # ocekavany zustatek po odeslani platby
        self.builtin.set_suite_variable('${USER_BALANCE}', expected_balance)    # nastaveni noveho zustatku
        logging.warning(f'send-money: check-po-platbe: ${expected_balance/100:,}')
        assert resp_balance == expected_balance, f"err: zustatek z api {resp_balance} nesedi s ocekavanym zustatkem " \
                                                 f"{expected_balance}"
        logging.warning(f"send-money: doslo k uspesnemu odeslani {amount} $ na ucet prijemce")

    def _get_receiver_id_from_api_resp(self, users_list, name):
        """Metoda prohleda python slovnik 'users_list' a na zaklade jmena prijemce 'name' vrati jeho id jako
        'receiver_id'. Pokud nebylo 'name' predano jako argument KW 'get receiver id', potom se 'name' nacte z
        testovacich dat.

        :param users_list: python slovnik jako odpoved z api /users obsahujici seznam pratel uzivatele
        :param name: jmeno prijemce, jemuz se odeslou penize
        """
        receiver_id = None
        if name is not None:
            receiver_name = name
        else:
            receiver_name = dataprovider.get_var(self.builtin.get_variable_value('${SEND_MONEY}'), 'receiver_name')
        users_list_len = len(users_list['results'])
        for i in range(users_list_len):
            if users_list['results'][i]['username'] == receiver_name:
                receiver_id = users_list['results'][i]['id']    # ulozeni receiverId prijemce
        assert receiver_id, f'err: jmeno prijemce: {receiver_name} neni v seznamu pratel uzivatele'
        logging.warning(f'send-money: jmeno prijemce ma receiver-id: {receiver_id}')
        return receiver_id
