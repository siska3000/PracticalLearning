import logging
import pandas as pd

from Processors.EntityProcesor import EntityProcessor
from FetchClass import SWAPIClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class SWAPIDataManager:
    def __init__(self, client: SWAPIClient):
        self.client = client
        self.df_list = {}
        self.processors = {}

    def register_processor(self, endpoint: str, processor: EntityProcessor):
        self.processors[endpoint] = processor

    def fetch_entity(self, endpoint: str):
        raw_data = self.client.fetch_json(endpoint)
        self.df_list[endpoint] = pd.DataFrame(raw_data)
        logger.info(f"Отримано {len(raw_data)} записів для {endpoint}. Колонки: {self.df_list[endpoint].columns.tolist()}")

    def apply_filter(self, endpoint: str, columns_to_drop: list):
        if endpoint in self.df_list:
            self.df_list[endpoint] = self.df_list[endpoint].drop(columns=columns_to_drop, errors='ignore')
            logger.info(f'Deleted a {columns_to_drop} from {self.df_list}')
        else:
            logger.info(f'Data for {endpoint} not found')

    def save_to_excel(self, file_name):
        output_file = file_name

        logger.info(f"Запис даних у Excel файл: {output_file}")
        with pd.ExcelWriter(output_file) as writer:
            for endpoint, df in self.df_list.items():
                df.to_excel(writer, sheet_name=endpoint, index=False)  # Запис  DataFrame

        logger.info("Дані успішно записано у Excel.")
