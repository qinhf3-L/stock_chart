import os

from sqlalchemy import create_engine
from sqlalchemy.types import NVARCHAR

MYSQL_HOST = os.environ.get('MYSQL_HOST') if (os.environ.get('MYSQL_HOST') != None) else "localhost:3306"
MYSQL_USER = os.environ.get('MYSQL_USER') if (os.environ.get('MYSQL_USER') != None) else "root"
MYSQL_PWD = os.environ.get('MYSQL_PWD') if (os.environ.get('MYSQL_PWD') != None) else "root"
MYSQL_DB = os.environ.get('MYSQL_DB') if (os.environ.get('MYSQL_DB') != None) else "stock_data"

MYSQL_CONN_URL = "mysql+mysqldb://" + MYSQL_USER + ":" + MYSQL_PWD + "@" + MYSQL_HOST + "/" + MYSQL_DB + "?charset=utf8mb4"


def engine():
    """
    info: define engine
    """
    engine = create_engine(
        MYSQL_CONN_URL,
        encoding='utf8', convert_unicode=True, echo=False)
    return engine