import _common.libraries.factory.concretefactory as concretefactory


class Notifications:
    """Klicova slova pro praci s notifikacemi."""

    def __init__(self):
        self.factory = concretefactory.ConcreteFactory()
        self.api = self.factory.create_http_requests
        self.builtin = self.factory.create_robot_builtin
        self.dfr = self.factory.create_data_for_request
        self.dataprovider = self.factory.get_dataprovider
        self.logging = self.factory.get_logging

        self.notif_dict = None

    def get_notifications_list(self):
        """KW vraci python slovnik se vsemi notifikacemi prihlaseneho uzivatele pomoci GET /notifications."""
        # prepare-test-data
        request_method = self.dfr.get_request_method('${TD_GET_NOTIFS_LIST}')
        request_url = self.dfr.get_request_url('${API_NAME}', '${TD_GET_NOTIFS_LIST}')
        resp = self.api.send_request(request_method, request_url)
        self.notif_dict = resp.json()
        self.logging.warning(f'Slovnik ma: {len(self.notif_dict["results"])} notifikaci')
        return self.notif_dict

    def delete_notifications(self, name=None, cnt=None):
        """KW smaze 'cnt' notifikaci prihlaseneho uzivatele podle jmena 'name' v notifikaci. Notifikace se mazou pomoci
        volani PATCH /notifications/{notification_id}.

        :param name: jmeno uvedene v notifikaci
        :param cnt: pocet notifikaci ke smazani: jednotlive [int] / 'all'[str]
        """
        name = name if name is not None else \
            self.dataprovider.get_var(self.builtin.get_variable_value('${TD_DEL_NOTIFS}'), 'name')
        cnt = cnt if cnt is not None else \
            self.dataprovider.get_var(self.builtin.get_variable_value('${TD_DEL_NOTIFS}'), 'cnt')
        notif_dict = self._get_notif_dict()
        # zjisti, jestli je slovnik s notifikacemi prazdny a pokud ano test zastavi, protoze neni co mazat
        assert self._is_notif_dict_empty(name, notif_dict), f'err: nejsou testovaci data pro: {name}, test konci.'
        # ulozi pocet notifikaci s vybranym jmenem pred mazanim notifikaci
        notif_cnt_before = self._get_notif_cnt_by_name(name, notif_dict)
        # vytvori novy slovnik pouze s notifikacemi se jmenem 'name'
        notif_dict_single = self._get_notif_dict_single(name, notif_dict)
        # na zaklade 'cnt' smaze n anebo vsechny notifikace podle vybraneho jmena
        self._dismiss_notification(name, notif_dict_single, cnt)
        # send-request: prenacte seznam notifikaci uzivatele pomoci GET /notifications
        notif_dict = self.get_notifications_list()
        # ulozi pocet notifikaci s vybranym jmenem po smazani notifikaci
        notif_cnt_after = self._get_notif_cnt_by_name(name, notif_dict)
        # check: overi, jestli doslo ke smazani pozadovaneho poctu notifikaci s vybranym jmenem
        self._check_notif(notif_cnt_before, notif_cnt_after, name, cnt)

    def _is_notif_dict_empty(self, name, notif_dict):
        """Metoda nejprve overi, jestli je slovnik s notifikacemi 'notif_dict' prazdny. Pokud ne, potom dale overi,
        jestli ve slovniku existuji notifikace se jmenem 'name', ktere se maji smazat. Pokud je slovnik prazdny anebo
        pokud neobsahuje notifikace se jmenem 'name', potom metoda vraci False a test konci, jelikoz neni co mazat.
        """
        return False if len(notif_dict['results']) == 0 else self._get_notif_cnt_by_name(name, notif_dict) > 0

    def _get_notif_cnt_by_name(self, name, notif_dict):
        """Metoda projde slovnik 'notif_dict' a vrati pocet notifikaci se jmenem 'name'."""
        notif_list = [s for s in notif_dict['results'] if name in s['userFullName']]
        if len(notif_list) == 0:
            self.logging.warning(f'del-notif: uzivatel nema zadne notifikace od: {name}')
        return len(notif_list)

    @staticmethod
    def _get_notif_dict_single(name, notif_dict):
        """Metoda vraci novy python slovnik, ktery obsahuje pouze notifikace s jedinym jmenem."""
        notif_dict_single = [s for s in notif_dict['results'] if name in s['userFullName']]
        return {'results': notif_dict_single}

    def _dismiss_notification(self, name, notif_dict_single, cnt):
        """Metoda odstrani jednu anebo vice notifikaci 'cnt' pro vybrane jmeno 'name' uvedene v notifikaci. Na vstupu
        je slovnik s notifikacemi, ktery obsahuje pouze notifikace s jedinym jmenem. Notifikace se mazou po jedne pomoci
        volani PATCH /notifications/{notification_id}.
        """
        # prepare-test-data
        request_method = self.dfr.get_request_method('${TD_DEL_NOTIFS}')
        request_url = self.dfr.get_request_url('${API_NAME}', '${TD_DEL_NOTIFS}')
        request_headers = self.dfr.get_request_headers('${TD_DEL_NOTIFS}')
        request_body = self.dfr.get_request_body('${TD_DEL_NOTIFS}')
        _notif_dict_id = "notif_dict_single['results'][i]['id']"
        _notif_dict_uname = "notif_dict_single['results'][i]['userFullName']"
        notif_dict_len = len(notif_dict_single['results'])
        if cnt == 'all':
            pass
        elif notif_dict_len - cnt >= 0:
            notif_dict_len = cnt
        # mazani notifikaci podle 'id' notifikace
        i = None
        for i in range(notif_dict_len):
            request_body['id'] = eval(_notif_dict_id)
            self.logging.warning(f"del-notif: mazu notifikaci se jmenem: {eval(_notif_dict_uname)}")
            self.logging.warning(f"del-notif: mazu notifikaci s id: {eval(_notif_dict_id)}")
            # send-request: pro kazdou notifikaci se posle jeden request PATCH /notifications/{notification_id}
            self.api.send_request(request_method, request_url.format(eval(_notif_dict_id)), request_body,
                                  headers=request_headers)
        self.logging.warning(f'del-notif: smazano: {i+1} notifikaci od: {name}')

    @staticmethod
    def _check_notif(notif_cnt_before, notif_cnt_after, name, cnt):
        """Metoda overi, jestli doslo ke smazani vsech notifikaci pro vybrane jmeno a v pozadovanem poctu."""
        if cnt == 'all':
            assert notif_cnt_after == 0, f'err: notifikace uzivatele {name} se nesmazaly'
        else:
            if notif_cnt_before - cnt >= 0:
                assert notif_cnt_after == (notif_cnt_before - cnt), f'err: #notif-pred: {notif_cnt_before}, ' \
                                                                    f'#notif-po: {notif_cnt_after}'
            else:
                assert notif_cnt_after == 0, f'err: #notif-pred: {notif_cnt_before}, #notif-po: {notif_cnt_after}'

    def _get_notif_dict(self):
        """Metoda vraci python slovnik s notifikacemi uzivatele. Nejdrive se pokusi vratit slovnik ulozeny v ramci KW
        'get notifications list', pokud tento neexistuje, vygeneruje novy slovnik.
        """
        if self.notif_dict:
            self.logging.warning(f"del-notif: slovnik 'notif_dict' byl ulozen v ramci KW 'get notifications list'")
            return self.notif_dict
        else:
            self.logging.warning(f"del-notif: generuju novy slovnik s notifikacemi: 'notif_dict'")
            return self.get_notifications_list()
