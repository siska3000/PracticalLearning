import pandas as pd
import logging

from FetchClass import SWAPIClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class ExcelSWAPIClient(SWAPIClient):
    def __init__(self, path: str):
        """
        Ініціалізація з шляхом до Excel-файлу.
        """
        super().__init__(path)
        self.data = pd.read_excel(path, sheet_name=None)

    def fetch_json(self, endpoint: str) -> list:
        """
        Завантажує дані з Excel-файлу для вказаного endpoint.

        :param endpoint: Назва листа в Excel (наприклад, "people")
        :return: список всіх сутностей у вигляді JSON
        """
        if endpoint not in self.data:
            logger.warning(f"Endpoint {endpoint} not found in {self.path}")
            return []

        return self.data[endpoint].to_dict(orient='records')
