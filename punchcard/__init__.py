import models

from punchcard.constants import DATABASE_PATH

DATABASE_PATH.mkdir(parents=True, exist_ok=True)
db = peewee.SqliteDatabase(DATABASE_PATH / "punchcard.db")
