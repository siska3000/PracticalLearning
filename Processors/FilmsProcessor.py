import pandas as pd
from Processors.EntityProcesor import EntityProcessor


class FilmsProcessor(EntityProcessor):
    def process(self, json_data: list) -> pd.DataFrame:
        df = pd.DataFrame(json_data)
        df['release_year'] = pd.to_datetime(df['release_date']).dt.year
        return df
