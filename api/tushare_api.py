import tushare as ts
import configparser as cp
import pandas as pd
from tools import utils
import time
import os


class TushareAPI:

    def __init__(self):
        config = cp.ConfigParser()
        config_path = os.path.join(utils.get_root_path(), 'config', 'stock.config')
        config.read(config_path, encoding='utf-8-sig')

        ts.set_token(config['TuShare']['token'])

        self.pro = ts.pro_api()

    def get_tickers_cn(self):
        columns = 'ts_code,symbol,name,area,industry,market,exchange,list_status,list_date,delist_date'
        df = self.pro.stock_basic(exchange='', list_status='L', fields=columns, offset=5397)
        return df

    def get_tickers_hk(self):
        df = self.pro.hk_basic(list_status='L')
        return df

    def get_tickers_us(self):
        all_data = []
        offset = 0
        limit = 5000
        requests_made = 0  # request number

        while True:
            if requests_made >= 2:
                # 2 request per minute, wait for 60 secs
                time.sleep(60)
                requests_made = 0  # reset counter

            df = self.pro.us_basic(offset=offset, limit=limit)
            requests_made += 1  # 请求计数加1

            if df.empty:
                break  # if no more data, break the loop

            # process data
            df = df.dropna(subset=['ts_code'])
            df['delist_date'] = df['delist_date'].replace(pd.NaT, None)
            df['delist_date'] = pd.to_datetime(df['delist_date'], format='%Y%m%d', errors='coerce')
            df['delist_date'] = df['delist_date'].where(pd.notnull(df['delist_date']), None)

            all_data.append(df)
            offset += limit  # update offset

        # 合并所有数据
        if all_data:
            return pd.concat(all_data, ignore_index=True)
        return pd.DataFrame()

