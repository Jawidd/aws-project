from psycopg_pool import ConnectionPool
import os


# connection_url = os.getenv("CONNECTION_URL_DOCKER") #dev
connection_url = os.getenv("AWS_RDS_PSQL_CONNECTION") #prod

pool = ConnectionPool(connection_url)

