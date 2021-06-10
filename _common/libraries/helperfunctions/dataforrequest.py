import _common.libraries.factory.concretefactory as concretefactory


class DataForRequest:
    """Pomocna trida, ktera vraci testovaci data pro volani jednotlivych http requestu. Data se nacitaji pomoci metod
    data provideru s parametry: 'td', ktery urcuje cestu k testovacim datum pro konkretni test (pomoci teckove notace)
    v syntaxi robota: ${promenna} a 'api_name', ktery urcuje nazev api, pro ktere se vrati prislusne URL.
    """
    def __init__(self):
        self.factory = concretefactory.ConcreteFactory()
        self.builtin = self.factory.create_robot_builtin
        self.dataprovider = self.factory.get_dataprovider

    def get_request_body(self, td):
        return self.dataprovider.get_var(self.builtin.get_variable_value(td), 'request_body')

    def get_request_headers(self, td):
        return self.dataprovider.get_var(self.builtin.get_variable_value(td), 'request_headers')

    def get_request_method(self, td):
        return self.dataprovider.get_var(self.builtin.get_variable_value(td), 'request_method')

    def get_request_url(self, api_name, td):
        return self.dataprovider.get_api_url(self.builtin.get_variable_value(api_name),
                                             self.dataprovider.get_var(self.builtin.get_variable_value(td), 'endpoint'))
