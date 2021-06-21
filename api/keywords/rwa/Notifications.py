import _common.libraries.factory.concretefactory as concretefactory


class Notifications:
    """Klicova slova pro praci s notifikacemi."""

    def __init__(self):
        self.factory = concretefactory.ConcreteFactory()
        self.api = self.factory.create_http_requests
        self.builtin = self.factory.create_robot_builtin
        self.drq = self.factory.create_data_for_request
        self.dataprovider = self.factory.get_dataprovider
        self.logging = self.factory.get_logging

        self.notif_dict = None

    def get_notifications_list(self):
        """KW vraci python slovnik se vsemi notifikacemi prihlaseneho uzivatele pomoci GET /notifications."""
        # prepare-test-data
        request_method = self.drq.get_request_method('${TD_GET_NOTIFS_LIST}')
        request_url = self.drq.get_request_url('${API_NAME}', '${TD_GET_NOTIFS_LIST}')
        # send-request: vrati vsechny notifikace prihlaseneho uzivatele pomoci GET /notifications
        resp = self.api.send_request(request_method, request_url)
        # check: overi, ze obsah odpovedi je validni JSON
        self.notif_dict = resp.json()
        self.logging.warning(f'get-notif-list: uzivatel ma: {len(self.notif_dict["results"])} notifikaci')
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
        # nacte slovnik s notifikacemi uzivatele
        notif_dict = self._get_notif_dict()
        # overi, jestli je slovnik s notifikacemi prazdny a pokud ano test zastavi, protoze neni co mazat
        self._is_notif_dict_empty(name, notif_dict)
        # vytvori python list obsahujici notifikace (python slovniky) s jedinym jmenem 'name'
        notif_list_one_name = self._get_notif_list_one_name(name, notif_dict)
        # ulozi pocet notifikaci s vybranym jmenem pred mazanim notifikaci
        notif_cnt_before = len(notif_list_one_name)
        # na zaklade 'cnt' smaze n anebo vsechny notifikace pro vybrane jmeno
        self._dismiss_notification(name, notif_list_one_name, cnt)
        # send-request: prenacte seznam notifikaci uzivatele pomoci GET /notifications
        notif_dict = self.get_notifications_list()
        # updatuje python list obsahujici notifikace (python slovniky) s jedinym jmenem 'name'
        notif_list_one_name = self._get_notif_list_one_name(name, notif_dict)
        # ulozi pocet notifikaci s vybranym jmenem po smazani notifikaci
        notif_cnt_after = len(notif_list_one_name)
        # check: overi, jestli doslo ke smazani pozadovaneho poctu notifikaci s vybranym jmenem
        self._check_notif(notif_cnt_before, notif_cnt_after, name, cnt)

    def _is_notif_dict_empty(self, name, notif_dict):
        """Metoda nejprve overi, jestli je slovnik s notifikacemi 'notif_dict' prazdny. Pokud ne, potom dale overi,
        jestli ve slovniku existuji notifikace se jmenem 'name', ktere se maji smazat. Pokud je slovnik prazdny anebo
        pokud neobsahuje notifikace se jmenem 'name', potom test konci, jelikoz neni co mazat.

        :param name: jmeno uvedene v notifikaci
        :param notif_dict: python slovnik s notifikacemi uzivatele: {results: [, ...]}
        """
        self.builtin.skip_if(len(notif_dict['results']) == 0, 'err-del-notif: uzivatel nema zadnou notifikaci')
        self.builtin.skip_if(len(self._get_notif_list_one_name(name, notif_dict)) == 0, f'err-del-notif: uzivatel nema '
                                                                                        f'zadnou notifikaci od: {name}')

    @staticmethod
    def _get_notif_list_one_name(name, notif_dict):
        """Metoda vraci python list, jehoz prvky jsou python slovniky (notifikace) s jedinym jmenem 'name'."""
        notif_list_one_name = [m for m in notif_dict['results'] if name in m['userFullName']]
        return notif_list_one_name

    def _dismiss_notification(self, name, notif_list_one_name, cnt):
        """Metoda odstrani jednu anebo vice notifikaci 'cnt' pro vybrane jmeno 'name' uvedene v notifikaci. Na vstupu
        je slovnik s notifikacemi, ktery obsahuje pouze notifikace s jedinym jmenem. Notifikace se mazou po jedne pomoci
        volani PATCH /notifications/{notification_id}.

        :param name: jmeno uvedene v notifikaci
        :param notif_list_one_name: python list obsahujici notifikace (python slovniky) s jedinym jmenem 'name'
        :param cnt: pocet notifikaci ke smazani: vsechny / jednotlive: [int] / 'all'[str]
        """
        # prepare-test-data
        request_method = self.drq.get_request_method('${TD_DEL_NOTIFS}')
        request_url = self.drq.get_request_url('${API_NAME}', '${TD_DEL_NOTIFS}')
        request_headers = self.drq.get_request_headers('${TD_DEL_NOTIFS}')
        request_body = self.drq.get_request_body('${TD_DEL_NOTIFS}')
        notif_id = "notif_list_one_name[i]['id']"
        notif_uname = "notif_list_one_name[i]['userFullName']"
        notif_list_len = len(notif_list_one_name)
        if cnt == 'all':
            pass
        elif notif_list_len - cnt >= 0:
            notif_list_len = cnt
        # mazani notifikaci podle 'id' notifikace
        i = 0
        for i in range(notif_list_len):
            request_body['id'] = eval(notif_id)
            self.logging.warning(f"del-notif: mazu notifikaci se jmenem: {eval(notif_uname)}")
            self.logging.warning(f"del-notif: mazu notifikaci s id: {eval(notif_id)}")
            # send-request: pro kazdou notifikaci se posle jeden request PATCH /notifications/{notification_id}
            self.api.send_request(request_method, request_url.format(eval(notif_id)), request_body,
                                  headers=request_headers)
        self.logging.warning(f'del-notif: smazano: {i+1} notifikaci od: {name}')

    @staticmethod
    def _check_notif(notif_cnt_before, notif_cnt_after, name, cnt):
        """Metoda overi, jestli doslo ke smazani vsech notifikaci pro vybrane jmeno a v pozadovanem poctu."""
        if cnt == 'all':
            assert notif_cnt_after == 0, f'err-del-notif: notifikace uzivatele {name} se nesmazaly'
        else:
            if notif_cnt_before - cnt >= 0:
                assert notif_cnt_after == (notif_cnt_before - cnt), f'err-del-notif: #notif-pred: ' \
                                                                    f'{notif_cnt_before}, #notif-po: {notif_cnt_after}'
            else:
                assert notif_cnt_after == 0, f'err-del-notif: #notif-pred: {notif_cnt_before}, #notif-po: ' \
                                             f'{notif_cnt_after}'

    def _get_notif_dict(self):
        """Metoda vraci python slovnik s notifikacemi uzivatele. Nejdrive se pokusi vratit slovnik ulozeny v ramci
        volani KW 'get notifications list'. Pokud tento neexistuje, vygeneruje se novy.
        """
        if self.notif_dict:
            self.logging.warning(f"del-notif: slovnik 'notif_dict' byl ulozen v ramci KW 'get notifications list'")
            return self.notif_dict
        else:
            self.logging.warning(f"del-notif: generuju novy slovnik s notifikacemi: 'notif_dict'")
            return self.get_notifications_list()
