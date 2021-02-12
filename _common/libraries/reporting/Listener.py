import logging
import reporting


class Listener:
    """Robot vola metody Listeneru vzdy po dobehnuti kazdeho testu / testovaci sady. Predava parametry jednotlivych
    testu, napr. stav testu (pass/fail), delku behu testu, ..., pro dalsi zpracovani, napr. odeslani vysledku do
    reportingoveho nastroje.
    """
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, *args):   # moznost vlozeni argumentu do listeneru z CLI napr: .... Listener.py:arg1:arg2
        self.args = args
        logging.warning(f'Argumenty listeneru: {self.args}\n')
        self.test_names = []
        self.test_statuses = []

    def end_test(self, name, result):
        """Robot vola metodu end_test vzdy po ukonceni kazdeho testu. Metoda uklada nazvy vsech spustenych testu vcetne
        jejich stavu PASS / FAIL.
        """
        self.test_names.append(result.name)
        self.test_statuses.append(result.status)

    def end_suite(self, name, result):
        """Robot vola metodu end_suite vzdy po ukonceni vsech testu v testovaci sade. Metoda nastavi konfiguraci pro
        reportingovy nastroj podle typu testu (api / ui) a potom ho zavola.
        """
        cfg = reporting.config
        # do konfigurace reportovaciho nastroje nastavi jmena a jim odpovidajici stavy testu (PASS / FAIL)
        for i in range(len(self.test_names)):
            n = cfg['data']['labels']
            n.append(self.test_names[i])
            if self.test_statuses[i] == 'FAIL':
                f1 = cfg['data']['datasets'][0]['data']
                f1.append(1)
                f2 = cfg['data']['datasets'][1]['data']
                f2.append(0)
            else:
                p1 = cfg['data']['datasets'][1]['data']
                p1.append(1)
                p2 = cfg['data']['datasets'][0]['data']
                p2.append(0)
        reporting.report_results(cfg)
