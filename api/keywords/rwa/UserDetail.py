import _common.libraries.factory.concretefactory as concretefactory


class UserDetail:
    """Klicova slova pro ziskani detailu prihlaseneho uzivatele anebo zvoleneho kamarada."""

    def __init__(self):
        self.factory = concretefactory.ConcreteFactory()
        self.api = self.factory.create_http_requests
        self.builtin = self.factory.create_robot_builtin
        self.drq = self.factory.create_data_for_request
        self.dataprovider = self.factory.get_dataprovider
        self.logging = self.factory.get_logging

    def get_user_detail(self, key):
        """Metoda hleda zvoleny klic 'key' v python slovniku v odpovedi z GET /checkAuth. Pokud je klic ve slovniku
        nalezen, metoda ho vrati, v opacnem pripade volani metody vyvola vyjimku.

        :param key: klic v python slovniku, ke kteremu se, v odpovedi z GET /checkAuth, vyhleda odpovidajici hodnota
        """
        # prepare-test-data
        request_method = self.drq.get_request_method('${TD_GET_USER_DETAIL}')
        request_url = self.drq.get_request_url('${API_NAME}', '${TD_GET_USER_DETAIL}')
        # send-request: z api GET /checkAuth ziska detail prihlaseneho uzivatele
        resp = self.api.send_request(request_method, request_url)
        resp_json = resp.json()
        # check: overi, ze zadany klic existuje v odpovedi z GET /checkAuth a pokud ano, potom vypise jeho hodnotu
        user_detail = [v for k, v in resp_json['user'].items() if k == key]
        user_detail = user_detail[0] if user_detail != [] else False
        assert user_detail, f'err-get-user-detail: pozadovany klic "{key}" neexistuje v odpovedi z api'
        self.logging.warning(f"get-user-detail: detail prihlaseneho uzivatele {resp_json['user']['username']}: "
                             f"{key} = {user_detail}")
        return user_detail

    def get_mate_detail(self, key, name):
        """Metoda vraci detail vybraneho kamarada prihlaseneho uzivatele zavolanim GET /users.

        :param name: jmeno kamarada, pro nejz se vrati detail
        :param key: klic v python slovniku, ke kteremu se, v odpovedi z GET /users, vyhleda odpovidajici hodnota
        """
        # prepare-test-data
        request_method = self.drq.get_request_method('${TD_GET_MATE_DETAIL}')
        request_url = self.drq.get_request_url('${API_NAME}', '${TD_GET_MATE_DETAIL}')
        # send-request: z api ziska seznam pratel, vcetne vsech detailu, pomoci GET /users
        resp = self.api.send_request(request_method, request_url)
        mates_list = resp.json()  # seznam pratel prihlaseneho uzivatele jako python slovnik
        # check: v odpovedi z api overi existenci pozadovaneho klice 'key'
        assert any(key in m for m in mates_list['results']), f'err-get-mate-detail: pozadovany klic "{key}" neexistuje'
        # check: v seznamu pratel najde kamarada se jmenem 'name' a pokud existuje, vrati pozadovany detail 'key'
        mate_detail = [m[key] for m in mates_list['results'] if m['username'] == name]
        mate_detail = mate_detail[0] if mate_detail != [] else False
        assert mate_detail, f'err-get-mate-detail: {name} neni v seznamu pratel prihlaseneho uzivatele'
        self.logging.warning(f'get-mate-detail: detail kamarada {name}: {key} = {mate_detail}')
        return mate_detail
