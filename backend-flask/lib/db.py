from psycopg_pool import ConnectionPool
import os


connection_url = os.getenv("CONNECTION_URL_DOCKER")
pool = ConnectionPool(connection_url)

