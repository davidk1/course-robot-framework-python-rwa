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

    def end_test(self, data, result):
        """Robot zavola metodu end_test vzdy po ukonceni kazdeho testu. Metoda pro kazdy test ulozi nazev testu vcetne
        jeho stavu PASS / FAIL.

        :param data: objekt s vlastnostmi konkretniho testu
        :param result: objekt s vysledky konkretniho testu
        """
        self.test_names.append(data.name)
        self.test_statuses.append(result.status)

    def end_suite(self, data, result):
        """Robot zavola metodu end_suite vzdy po ukonceni vsech testu v testovaci sade. Metoda nejdrive upravi vychozi
        konfiguraci reportingoveho nastroje, tzn. doplni nazvy a stavy exekuce vsech spustenych testu. Potom se nastroj
        zavola a tim se odeslou vysledky testu, ktere jsou dostupne pres http protokol na adrese uvedene v logu kazdeho
        testu jako 'reporting-url' a 'reporting-qr-kod'.

        :param data: objekt s vlastnostmi konkretni testovaci sady
        :param result: objekt s vysledky konkretni testovaci sady
        """
        reporting.report_results(self.test_names, self.test_statuses)
