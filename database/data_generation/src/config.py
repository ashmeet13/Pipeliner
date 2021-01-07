import os

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
DATABASE = os.getenv("DATABASE", "online_store")
PSQL_USERNAME = os.getenv("PSQL_USERNAME", "postgres")
PSQL_PASSWORD = os.getenv("PSQL_PASSWORD", "postgres")

BACKFILL_DAYS = int(os.getenv("BACKFILL_DAYS", "1"))

VARIABLE_INSERT_DELAY_START = int(os.getenv("VARIABLE_INSERT_DELAY_START", "1"))
VARIABLE_INSERT_DELAY_STOP = int(os.getenv("VARIABLE_INSERT_DELAY_STOP", "5")) + 1
