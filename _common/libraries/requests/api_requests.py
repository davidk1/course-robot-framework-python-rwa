import logging
import requests


def send_request(session, method, url, body=None, **kwargs):
    """Implementace vybranych http metod pro volani sluzeb rest/soap.
    :param session: unikatni session-id pro vsechny volani v ramci test suite
    :param method: http metoda (get / post / patch)
    :param url: url konkretniho api
    :param body: telo http requestu
    """
    resp = None
    headers = None
    allow_redirects = None

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
        # logging.warning(f"resp-status-code: {service_url.split('//')[1][14:]} -> {resp.status_code}")
    except requests.ConnectionError as e:
        logging.warning(f'Connection error, viz vyjimka: {e.args}')
        raise e
    return resp
