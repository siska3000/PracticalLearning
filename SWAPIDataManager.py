import logging
import pandas as pd

from FetchClass import SWAPIClient
from interfaces import DataFetcher, DataProcessor, DataSaver


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class SWAPIDataManager(DataFetcher, DataProcessor, DataSaver):
    def __init__(self, client: SWAPIClient):
        self.client = client
        self.df_list = {}
        self.processors = {}

    def fetch_entity(self, endpoint: str):
        raw_data = self.client.fetch_json(endpoint)

        if endpoint in self.processors:
            processor = self.processors[endpoint]
            processed_data = processor.process(raw_data)
            self.df_list[endpoint] = pd.DataFrame(processed_data)
            logger.info(f"Processed {len(processed_data)} records for {endpoint} using a processor.")
        else:
            self.df_list[endpoint] = pd.DataFrame(raw_data)
            logger.info(f"Retrieved {len(raw_data)} records for {endpoint}. Columns: {self.df_list[endpoint].columns.tolist()}")

    def register_processor(self, endpoint: str, processor):
        self.processors[endpoint] = processor

    def apply_filter(self, endpoint: str, columns_to_drop: list):
        if endpoint in self.df_list:
            self.df_list[endpoint] = self.df_list[endpoint].drop(columns=columns_to_drop, errors='ignore')
            logger.info(f"Deleted columns {columns_to_drop} from {endpoint} dataset")
        else:
            logger.warning(f"Data for {endpoint} not found")

    def save_to_excel(self, file_name: str):
        logger.info(f"Saving data to Excel file: {file_name}")
        with pd.ExcelWriter(file_name) as writer:
            for endpoint, df in self.df_list.items():
                df.to_excel(writer, sheet_name=endpoint, index=False)
        logger.info("Data successfully saved to Excel.")