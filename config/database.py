
import os

from databases import Database
from dotenv import load_dotenv
from sqlalchemy import URL

load_dotenv()

DATABASE_URL = URL.create(
    drivername="mysql+aiomysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "3308")),
    database=os.getenv("DB_NAME"),
)

database = Database(
    DATABASE_URL.render_as_string(
        hide_password=False
    )
)
