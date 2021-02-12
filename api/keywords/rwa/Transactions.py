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
        """KW z api ziska id-cko prijemce, jemuz se odeslou penize a ulozi ho jako 'receiver_id' pro pouziti v jinych
        KW. Pokud neni KW predany argument 'name', potom se 'receiver_id' vygeneruje na zaklade 'name' z testovacich
        dat. 'receiver_id' se ziska parsovanim odpovedi GET /users.
        """
        service_method = 'get'
        service_name = 'users'
        service_url = dataprovider.get_api_url(self.builtin.get_variable_value('${API_NAME}'), service_name)
        # send-request: z api ziska seznam pratel, vcetne vsech detailu, pomoci GET /users
        resp = send_request(self.session, service_method, service_url)
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
        service_method = 'post'
        service_name = 'transactions'
        service_url = dataprovider.get_api_url(self.builtin.get_variable_value('${API_NAME}'), service_name)
        service_body = dataprovider.get_var(self.builtin.get_variable_value('${SEND_MONEY}'), 'body')
        # prepare-request-body: upravi vychozi hodnoty parametru v testovacich datech
        service_body['senderId'] = self.builtin.get_variable_value('${USER_ID}')   # nacteni ${USER_ID} z KW login
        service_body['receiverId'] = self.get_receiver_id(name)
        if amount is not None:
            service_body['amount'] = amount
        # send-request: odesle platbu zavolanim POST /transactions
        resp = send_request(self.session, service_method, service_url, service_body)
        resp_json = resp.json()
        logging.warning(f'send-money-request: {service_body}')
        logging.warning(f'send-money-response: {resp_json}')
        logging.warning(f"sender-id: {service_body['senderId']}")
        logging.warning(f'receiver-id: {self.receiver_id}')
        # check: odpoved z api overi vuci parametru 'expected_response' v testovacich datech
        self._check_tx_response(service_body, resp_json)
        # check: kontrola aktualniho zustatku po odeslani platby
        self._check_current_balance(service_body['amount'])

    def _check_tx_response(self, service_body, resp_json):
        """Metoda overi ocekavany vysledek z testovacich dat vuci parametrum v odpovedi z api po odeslani platby.
        :param service_body: telo requestu odeslaneho v ramci platby pomoci POST /transactions [python dictionary]
        :param resp_json: telo response vracene z api po odeslani platby [python dictionary]
        """
        # nacteni template s ocekavanymi vysledky z testovacich dat a vyplneni parametru, kde je None
        expected_resp = dataprovider.get_var(self.builtin.get_variable_value('${SEND_MONEY}'), 'expected_response')
        expected_resp['transaction']['amount'] = service_body['amount'] * 100
        expected_resp['transaction']['receiverId'] = service_body['receiverId']
        expected_resp['transaction']['senderId'] = service_body['senderId']
        expected_resp['transaction']['description'] = service_body['description']
        logging.warning(f"expected_response: {expected_resp}")
        logging.warning(f"actual_response: {resp_json}")
        diff = DeepDiff(resp_json, expected_resp, exclude_paths={"root['transaction']['id']",
                                                                 "root['transaction']['uuid']",
                                                                 "root['transaction']['createdAt']",
                                                                 "root['transaction']['modifiedAt']"})
        assert diff == {}, f'Chyba po odeslani transakce: {diff}'

    def _check_current_balance(self, amount=None):
        """Nacte aktualni zustatek uzivatele zavolanim GET /checkAuth a overi, jestli doslo ke spravnemu odecteni
        castky po odeslani platby.
        """
        service_method = 'get'
        service_name = 'checkAuth'
        service_url = dataprovider.get_api_url(self.builtin.get_variable_value('${API_NAME}'), service_name)
        # send-request: ziska detail prihlaseneho uzivatele vcetne aktualniho zustatku na uctu zavolanim GET /checkAuth
        resp = send_request(self.session, service_method, service_url)
        resp_json = resp.json()
        # check: overi konecny zustatek po odeslani platby
        resp_balance = resp_json['user']['balance'] # aktualni zustatek vraceny z api
        expected_balance = self.builtin.get_variable_value('${USER_BALANCE}')    # zustatek nacteny v ramci loginu
        logging.warning(f'$ check-pred-platbou: {expected_balance}')  # zustatek pred odeslanim platby
        expected_balance = expected_balance - amount*100  # ocekavany zustatek po odeslani platby
        self.builtin.set_suite_variable('${USER_BALANCE}', expected_balance)    # nastaveni noveho zustatku
        logging.warning(f'$ check-po-platbe: {expected_balance}')
        assert resp_balance == expected_balance, f"Zustatek z api {resp_balance} nesedi s ocekavanym zustatkem " \
                                                 f"{expected_balance}"
        logging.warning(f"check-send-money: doslo k uspesnemu odeslani {amount} $ na ucet prijemce")

    def _get_receiver_id_from_api_resp(self, users_list, name):
        """Metoda prohleda python slovnik 'users_list' a na zaklade jmena prijemce 'name' vrati jeho id jako
        'receiver_id'. Pokud nebylo 'name' predano jako argument KW 'get receiver id', potom se 'name' nacte z
        testovacich dat.
        :param users_list: python slovnik jako odpoved z api obsahujici seznam pratel uzivatele
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
        assert receiver_id, f'check-get-receiver_id: jmeno prijemce: {receiver_name} neni v seznamu pratel uzivatele'
        logging.warning(f'check-get-receiver_id: jmeno prijemce ma receiver-id: {receiver_id}')
        return receiver_id
