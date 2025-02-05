import tushare as ts
import configparser as cp
from tools import utils
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
        df = self.pro.stock_basic(exchange='', list_status='L', fields=columns)
        return df

