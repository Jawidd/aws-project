from psycopg_pool import ConnectionPool
import os



connection_url = os.getenv("CONNECTION_URL") #prod

pool = ConnectionPool(connection_url)

