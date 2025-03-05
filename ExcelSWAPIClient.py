import pandas as pd
import logging

from DataProviderInterface import DataProviderInterface
from SWAPIClient import SWAPIClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class ExcelSWAPIClient(DataProviderInterface):
    def __init__(self, path: str):
        self.path = path
        self.data = pd.read_excel(path, sheet_name=None)

    def fetch_data(self, endpoint: str) -> list:
        """
        Завантажує дані з Excel-файлу для вказаного endpoint.

        :param endpoint: Назва листа в Excel (наприклад, "people")
        :return: список всіх сутностей у вигляді JSON
        """
        if endpoint not in self.data:
            logger.warning(f"Endpoint {endpoint} not found in {self.path}")
            return []

        return self.data[endpoint].to_dict(orient='records')
