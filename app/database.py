import pymysql
import pymysql.cursors
from app.config import *

def get_db_connection():
    return pymysql.connect(
        host=DATABASE_HOST,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        database=DATABASE_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )