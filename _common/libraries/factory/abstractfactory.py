from abc import ABC, abstractmethod


class AbstractFactory(ABC):
    @abstractmethod
    def create_auth(self):
        pass

    @abstractmethod
    def create_data_for_request(self):
        pass

    @abstractmethod
    def create_robot_builtin(self):
        pass

    @abstractmethod
    def get_comparator(self):
        pass

    @abstractmethod
    def get_dataprovider(self):
        pass

    @abstractmethod
    def get_requests(self):
        pass

    @abstractmethod
    def create_http_requests(self):
        pass

    @abstractmethod
    def create_api_session(self):
        pass

    @abstractmethod
    def get_logging(self):
        pass

    @abstractmethod
    def create_user_detail(self):
        pass
