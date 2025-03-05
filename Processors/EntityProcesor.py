from abc import abstractmethod

import pandas as pd


class EntityProcessor:
    @abstractmethod
    def process(self, json_data: list) -> pd.DataFrame:
        """Метод для обробки даних. Реалізується в дочірніх класах."""
        pass
