from .config import *
from .generator import DataGenerator
from .manager import DatabaseManager


def get_orders(manager: DatabaseManager):
    query = """
    SELECT item_id FROM item
    """

    return manager.select(query)


if __name__ == "__main__":
    manager = DatabaseManager(
        host=POSTGRES_HOST,
        database=DATABASE,
        user=PSQL_USERNAME,
        password=PSQL_PASSWORD,
    )

    generation_config = {
        "order_time": "GENERATOR__TIME_NOW",
        "item_id": get_orders(manager),
    }

    generator = DataGenerator(manager=manager, config=generation_config, table="orders")

    generator.start_generation(
        min_interval=VARIABLE_INSERT_DELAY_START,
        max_interval=VARIABLE_INSERT_DELAY_STOP,
        backfill_days=BACKFILL_DAYS,
    )
