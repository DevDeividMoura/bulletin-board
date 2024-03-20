from peewee import *
from config import DATA_DIR

DB = SqliteDatabase(f"{DATA_DIR}/webui.db")
DB.connect()