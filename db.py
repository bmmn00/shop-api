import os
from psycopg_pool import ConnectionPool
from dotenv import load_dotenv

load_dotenv()  # prod дээр .env байхгүй — юу ч хийхгүй өнгөрнө

pool = ConnectionPool(os.environ["DATABASE_URL"], open=True)

SCHEMA = """
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT,
    created_at DATE DEFAULT now()
);
"""


def query(sql, params=None):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            if cur.description is not None:
                return cur.fetchall()


def init_db():
    query(SCHEMA)
