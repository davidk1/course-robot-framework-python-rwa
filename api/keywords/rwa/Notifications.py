import logging
from robot.libraries.BuiltIn import BuiltIn
from _common.libraries.dataprovider import dataprovider
from _common.libraries.requests.api_requests import send_request


class Notifications:
    """Klicova slova pro praci s notifikacemi."""

    def __init__(self):
        self.builtin = BuiltIn()
        self.session = self.builtin.get_variable_value('${SESSION_ID}')
        self.notif_dict = None

    def get_notifications_list(self):
        """KW vraci python slovnik se vsemi notifikacemi prihlaseneho uzivatele pomoci GET /notifications."""
        request_method = 'get'
        service_name = 'notifications'
        request_url = dataprovider.get_api_url(self.builtin.get_variable_value('${API_NAME}'), service_name)
        resp = send_request(self.session, request_method, request_url)
        self.notif_dict = resp.json()
        return self.notif_dict

    def delete_notifications(self, name=None, notif_dict=None, cnt=None):
        """KW smaze 'cnt' notifikaci prihlaseneho uzivatele podle jmena 'name' v notifikaci. Notifikace se mazou pomoci
        volani PATCH /notifications/{notification_id}.

        :param name: jmeno uvedene v notifikaci
        :param notif_dict: python slovnik s notifikacemi prihlaseneho uzivatele: {'results': [,...]}
        :param cnt: pocet notifikaci ke smazani [pocet(int) / 'all'(string)]
        """
        name = name if name is not None else dataprovider.get_var(self.builtin.get_variable_value('${DEL_NOTIF}'),
                                                                  'name')
        cnt = cnt if cnt is not None else dataprovider.get_var(self.builtin.get_variable_value('${DEL_NOTIF}'), 'cnt')
        notif_dict = self._get_notif_dict(notif_dict)
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

    @staticmethod
    def _get_notif_cnt_by_name(name, notif_dict):
        """Metoda projde slovnik 'notif_dict' a vrati pocet notifikaci se jmenem 'name'."""
        notif_list = [s for s in notif_dict['results'] if name in s['userFullName']]
        if len(notif_list) == 0:
            logging.warning(f'del-notif: uzivatel nema zadne notifikace od: {name}')
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
        request_method = 'patch'
        service_name = 'notification_id'
        request_url = dataprovider.get_api_url(self.builtin.get_variable_value('${API_NAME}'), service_name)
        request_body = dataprovider.get_var(self.builtin.get_variable_value('${DEL_NOTIF}'), 'body')
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
            logging.warning(f"del-notif: mazu notifikaci se jmenem: {eval(_notif_dict_uname)}")
            logging.warning(f"del-notif: mazu notifikaci s id: {eval(_notif_dict_id)}")
            # send-request: pro kazdou notifikaci se posle jeden request PATCH /notifications/{notification_id}
            send_request(self.session, request_method, request_url.format(eval(_notif_dict_id)), request_body)
        logging.warning(f'del-notif: smazano: {i+1} notifikaci od: {name}')

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

    def _get_notif_dict(self, notif_dict):
        """Metoda vraci python slovnik s notifikacemi uzivatele. Nejdrive se pokusi vratit slovnik predany jako argument
        v KW 'delete notifications', pokud tento neexistuje, pokusi se vratit slovnik ulozeny v ramci KW
        'get notifications list'. Pokud ani tento neexistuje, vygeneruje novy slovnik s notifikacemi.
        """
        if notif_dict:
            logging.warning(f"del-notif: slovnik 'notif_dict' predan jako argument v KW 'delete ...'")
            self.notif_dict = notif_dict
            return notif_dict
        elif self.notif_dict:
            logging.warning(f"del-notif: slovnik 'notif_dict' ulozen v ramci KW 'get notifications list'")
            return self.notif_dict
        else:
            logging.warning(f"del-notif: generuju novy slovnik: 'notif_dict'")
            return self.get_notifications_list()
