from abc import ABC, abstractmethod


class DataProviderInterface(ABC):
    @abstractmethod
    def fetch_data(self, endpoint: str) -> list:
        pass
