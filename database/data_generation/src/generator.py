import datetime
import random
import time

from loguru import logger

from .manager import DatabaseManager


class DataGenerator:
    def __init__(self, manager: DatabaseManager, table, config):
        self.manager = manager
        self.config = config
        self.table = table

    def get_table_columns_string(self):
        stringify_cols = ", ".join(self.config.keys())
        table_columns = f"{self.table} ({stringify_cols})"
        return table_columns

    def _generator(self):
        query = f"INSERT INTO {self.get_table_columns_string()} VALUES"
        while True:
            value_to_insert = []
            for column in self.config.keys():
                if self.config[column] == "GENERATOR__TIME_NOW":
                    value_to_insert.append(datetime.datetime.utcnow())
                else:
                    value_to_insert.append(random.choice(self.config[column]))
            data_to_add = [tuple(value_to_insert)]
            self.manager.insert(query, data_to_add)
            logger.info(f"Inserted - {data_to_add}")
            time.sleep(random.choice(self.interval))

    def _backfill_generator(self, backfill_days):

        backfill_delta = datetime.timedelta(days=backfill_days)
        backfill_current_time = self.start_time - backfill_delta

        data_to_add = []

        while backfill_current_time < self.start_time:
            value_to_insert = []
            for column in self.config.keys():
                if self.config[column] == "GENERATOR__TIME_NOW":
                    value_to_insert.append(backfill_current_time)
                else:
                    value_to_insert.append(random.choice(self.config[column]))
            interval_delta = datetime.timedelta(seconds=random.choice(self.interval))
            backfill_current_time += interval_delta
            data_to_add.append(tuple(value_to_insert))

        query = f"INSERT INTO {self.get_table_columns_string()} VALUES"
        self.manager.insert(query, data_to_add)

    def start_generation(self, min_interval, max_interval, backfill_days=None):
        self.start_time = datetime.datetime.utcnow()
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.interval = list(range(min_interval, max_interval + 1))
        if backfill_days:
            self._backfill_generator(backfill_days)

        self._generator()
