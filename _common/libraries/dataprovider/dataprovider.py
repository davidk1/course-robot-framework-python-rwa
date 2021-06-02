import importlib

URLS = "_common.libraries.datasource.urls"    # cesta k modulu s konfiguraci baseurls a endpoints pro api a ui testy


def get_var(test_data_path, var):
    """Metoda vraci obsah konkretni promenne ze souboru s testovacimi daty.

    :param test_data_path: absolutni cesta k souboru s testovacimi daty (zapis pomoci teckove notace)
    :param var: nazev promenne, jejiz obsah se vrati ze souboru s testovacimi daty
    """
    test_data_module = importlib.import_module(test_data_path)
    var = getattr(test_data_module, var)
    return var


def get_base_url(name):
    """Metoda vraci base URL pro vybranou aplikaci / api.

    :param name: nazev aplikace
    """
    return get_var(URLS, 'baseurls')[name]


def get_api_url(api_name, endpoint):
    """Metoda vraci URL pro vybrane api.

    :param api_name: nazev api
    :param endpoint: nazev sluzby
    """
    baseurl = get_base_url(api_name)
    endpoint = get_var(URLS, 'endpoints')[api_name][endpoint]
    return baseurl + endpoint
