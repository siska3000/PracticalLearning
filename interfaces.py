from abc import ABC, abstractmethod


class DataFetcher(ABC):
    @abstractmethod
    def fetch_entity(self, endpoint: str):
        """Отримує сутність із вказаного джерела."""


class DataProcessor(ABC):
    @abstractmethod
    def apply_filter(self, endpoint: str, columns_to_drop: list):
        """Фільтрує дані, видаляючи непотрібні стовпці."""

    @abstractmethod
    def register_processor(self, entity: str, processor):
        """Реєструє процесор для обробки певної сутності."""


class DataSaver(ABC):
    @abstractmethod
    def save_to_excel(self, filename: str):
        """Зберігає дані у файл Excel."""
