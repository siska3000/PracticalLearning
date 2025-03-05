import pandas as pd

from Processors.EntityProcesor import EntityProcessor


class PeopleProcessor(EntityProcessor):
    def process(self, json_data: list) -> pd.DataFrame:
        df = pd.DataFrame(json_data)
        df['full_name'] = df['name']  # Наприклад, додавання нового поля
        return df
