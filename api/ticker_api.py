from database.repository import Repository
from api.tushare_api import TushareAPI


class TickerAPI:

    def __init__(self):
        self.repo = Repository()
        self.ts_api = TushareAPI()

    def update_cn_tickers(self):
        df = self.ts_api.get_tickers_cn()
        self.repo.insert(df, 'tickers_cn')


if __name__ == '__main__':
    ticker_api = TickerAPI()
    ticker_api.update_cn_tickers()