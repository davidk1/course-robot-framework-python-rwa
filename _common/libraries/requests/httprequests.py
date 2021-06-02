from abc import ABC, abstractmethod
import _common.libraries.factory.concretefactory as concretefactory


class BaseHTTPRequests(ABC):
    """Base class pro volani http requestu."""

    @abstractmethod
    def send_request(self, method, url, body=None, **kwargs):
        pass


class HTTPRequests(BaseHTTPRequests):
    """Implementace abstraktni metody 'send_request' pomoci knihovny 'requests'. Alternativni implementace lze vytvaret
    implementaci abstraktni metody v podtride, ktera dedi z abstraktni tridy 'BaseHTTPRequests'.
    """
    def __init__(self):
        self.factory = concretefactory.ConcreteFactory()

    def send_request(self, method, url, body=None, **kwargs):
        """Implementace vybranych http metod pro volani sluzeb rest/soap.

        :param method: http metoda (get / post / patch)
        :param url: url volaneho api
        :param body: telo http requestu
        """
        resp = None
        headers = None
        allow_redirects = None
        builtin = self.factory.create_robot_builtin
        logging = self.factory.get_logging
        requests = self.factory.get_requests
        session = builtin.get_variable_value('${SESSION_ID}')
        if kwargs:
            if 'headers' in kwargs.keys():
                headers = kwargs['headers']
            if 'allow_redirects' in kwargs.keys():
                allow_redirects = kwargs['allow_redirects']
        try:
            if method == 'get':
                resp = session.get(url=url, headers=headers)
            if method == 'post':
                resp = session.post(url=url, headers=headers, json=body, allow_redirects=allow_redirects)
            if method == 'patch':
                resp = session.patch(url=url, headers=headers, json=body)
            resp.raise_for_status()
        except requests.ConnectionError as e:
            logging.warning(f'Connection error, viz vyjimka: {e.args}')
            raise e
        return resp
