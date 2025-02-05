import pandas as pd
from sqlalchemy import text
import logging
from database.database import Database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 启用 SQLAlchemy 的 SQL 语句日志记录
sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
sqlalchemy_logger.setLevel(logging.INFO)


class Repository:

    def __init__(self):
        # 实例化数据库连接
        self.db = Database()

    def execute(self, sql):
        engine = self.db.get_connection()
        with engine.connect() as connection:
            connection.execute(text(sql))
            connection.commit()

    def insert(self, df, table_name):
        engine = self.db.get_connection()
        try:
            with engine.connect() as connection:
                logger.info("Database connection successful.")
                df.to_sql(table_name, connection, if_exists="append", index=False)
                logger.info(f"Data written to table {table_name} successfully.")
        except Exception as e:
            logger.error(f"Error writing to table {table_name}: {e}")

    def query(self, sql):
        engine = self.db.get_connection()
        df = pd.read_sql_query(sql, engine)
        return df

    def query_cn_tickers(self):
        sql = "select * from tickers_cn where list_status='L';"
        return self.query(sql)

    def query_hk_tickers(self):
        sql = "select * from tickers_hk where list_status='L';"
        return self.query(sql)

    def query_us_tickers(self):
        sql = "select * from tickers_us where list_status='L' and classify='EQ';"
        return self.query(sql)
