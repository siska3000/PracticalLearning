import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class ExcelSWAPIClient:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def fetch_json(self, endpoint: str) -> list:
        excel_data = pd.read_excel(self.file_path, sheet_name=None)
        available_sheets = excel_data.keys()

        if endpoint not in available_sheets:
            raise ValueError(f"Unknown endpoint: {endpoint}")

        df = excel_data[endpoint]
        logger.info(f"Читання даних з файлу {self.file_path}, лист {endpoint}")
        return df.to_dict(orient='records')
