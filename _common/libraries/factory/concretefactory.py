import logging
import requests
from requests import Session
from robot.libraries.BuiltIn import BuiltIn
from .abstractfactory import AbstractFactory
from _common.libraries.helperfunctions.dataforrequest import DataForRequest
from api.keywords.rwa.Auth import Auth
from api.keywords.rwa.UserDetail import UserDetail
from _common.libraries.dataprovider import dataprovider
from _common.libraries.helperfunctions.comparator import compare_results
from _common.libraries.requests.httprequests import HTTPRequests


class ConcreteFactory(AbstractFactory):
    """Trida implementuje property, ktere vraci zavislosti vyuzivane jednotlivymi klicovymi slovy a pomocnymi funkcemi.
    Property s prefixem 'create' vraci instanci konkretni tridy zatimco 'get' vraci konkretni modul (krome
    get_comparator, ktery vraci funkci).
    """
    @property
    def create_api_session(self):
        return Session()

    @property
    def create_auth(self):
        return Auth()

    @property
    def create_data_for_request(self):
        return DataForRequest()

    @property
    def create_http_requests(self):
        return HTTPRequests()

    @property
    def create_robot_builtin(self):
        return BuiltIn()

    @property
    def create_user_detail(self):
        return UserDetail()

    @property
    def get_comparator(self):
        return compare_results

    @property
    def get_dataprovider(self):
        return dataprovider

    @property
    def get_logging(self):
        return logging

    @property
    def get_requests(self):
        return requests
