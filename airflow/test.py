import time
from datetime import datetime, timedelta

import psycopg2
from loguru import logger


class DatabaseManager:
    def __init__(
        self, host: str, database: str, user: str, password: str, retry_count: int = 5
    ):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.retry_count = retry_count
        self._init_connection()

    def _init_connection(self):
        for _retry in range(self.retry_count):
            try:
                self.connection = psycopg2.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password,
                )
            except psycopg2.OperationalError as e:
                logger.exception("Database not up. Sleeping.")
                time.sleep(10)
            except Exception as e:
                logger.error("Error while strart up: " + str(e))
                exit()

    # def insert(self, query, args):
    #     cursor = self.connection.cursor()
    #     cursor.execute(query, args)
    #     self.connection.commit()
    #     cursor.close()

    def insert(self, query, data):
        cursor = self.connection.cursor()
        records_list_template = ",".join(["%s"] * len(data))
        query = "{} {}".format(query, records_list_template)
        cursor.execute(query, data)
        self.connection.commit()
        logger.info(f"Inserted {len(data)} points")
        cursor.close()

    def select(self, query, data):
        cursor = self.connection.cursor()
        cursor.execute(query, data)
        data = cursor.fetchall()
        cursor.close()
        return data


m = DatabaseManager(
    host="localhost", database="online_store", user="postgres", password="postgres"
)

stop = datetime.utcnow()
delta = timedelta(minutes=2)
start = stop - delta

print(start)
print(stop)

query = """SELECT AVG(item.item_price::numeric)
        FROM orders
        JOIN item ON orders.item_id = item.item_id
        WHERE orders.order_time>%s AND orders.order_time<=%s;"""

print(m.select(query, (start, stop)))
