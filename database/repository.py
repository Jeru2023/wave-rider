import pandas as pd
from sqlalchemy import text
import logging
from database.conn import Connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Repository:

    def __init__(self):
        # init db connection
        self.db = Connection()

    def execute(self, sql):
        engine = self.db.get_connection()
        with engine.connect() as connection:
            connection.execute(text(sql))
            connection.commit()

    def truncate_table(self, table_name):
        sql = f"truncate table {table_name}"
        self.execute(sql)

    def insert(self, df, table_name):
        engine = self.db.get_connection()
        try:
            with engine.connect() as connection:
                logger.info("Database connection successful.")
                df.to_sql(table_name, connection, if_exists="append", index=False)
                logger.info(f"Data written to table {table_name} successfully.")
        except Exception as e:
            logger.error(f"Error writing to table {table_name}: {e}")

    @staticmethod
    def get_realtime_table_by_region(region):
        if region == 'cn':
            return 'daily_prices_realtime_cn'
        elif region == 'us':
            return 'daily_prices_realtime_us'
        elif region == 'hk':
            return 'daily_prices_realtime_hk'
        else:
            return None

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

    @staticmethod
    def generate_ma_sql(table_name, period):
        sql = f"""
        SELECT AVG(close) FROM (
            SELECT close FROM {table_name} WHERE code = lp.code AND trade_date <= lp.trade_date
            ORDER BY trade_date DESC LIMIT {period}
        ) AS last_{period}_days
        """
        return sql

    def calculate_moving_averages_batch(self, region):
        table_name = self.get_realtime_table_by_region(region)
        if table_name is None:
            logger.error(f"Invalid region: {region}")
            return

        ma_20_sql = self.generate_ma_sql(table_name, 20)
        ma_50_sql = self.generate_ma_sql(table_name, 50)
        ma_150_sql = self.generate_ma_sql(table_name, 150)
        ma_200_sql = self.generate_ma_sql(table_name, 200)

        sql = f"""
               SELECT lp.code, lp.trade_date, lp.close as current_price,
               ({ma_20_sql}) AS ma_20, ({ma_50_sql}) AS ma_50,
               ({ma_150_sql}) AS ma_150, ({ma_200_sql}) AS ma_200,        
               (SELECT MAX(close) FROM {table_name} WHERE code = lp.code) AS high_of_52weeks,
               (SELECT MIN(close) FROM {table_name} WHERE code = lp.code) AS low_of_52weeks
               FROM (SELECT dsp.code, dsp.trade_date, dsp.close FROM {table_name} dsp
               WHERE dsp.trade_date = (SELECT MAX(trade_date) FROM {table_name} WHERE code = dsp.code)
               ) AS lp ORDER BY lp.code;
               """
        return self.query(sql)

    def delete_ma(self, region):
        sql = f"delete from moving_averages where region={region}"
        self.execute(sql)


if __name__ == '__main__':
    repo = Repository()
    df = repo.calculate_moving_averages_batch('cn')
