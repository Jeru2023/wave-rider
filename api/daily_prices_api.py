from database.repository import Repository
from api.tushare_api import TushareAPI
from api.ticker_api import TickerAPI
import logging
import numpy as np
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DailyPricesAPI:

    def __init__(self):
        self.repo = Repository()
        self.ts_api = TushareAPI()
        self.ticker_api = TickerAPI()

    def update_daily_price_realtime_cn(self):
        # get all cn tickers
        code_list = self.ticker_api.get_cn_tickers()
        total_codes = len(code_list)
        logger.info(f"Total codes to process: {total_codes}")

        # define batch size
        batch_size = 20

        # calculate number of batches
        num_batches = int(np.ceil(total_codes / batch_size))
        logger.info(f"Processing in {num_batches} batches, {batch_size} codes per batch")

        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
        end_date = datetime.now().strftime('%Y%m%d')

        # 分批处理
        for i in range(num_batches):
            # get current batch of code_list
            start_index = i * batch_size
            end_index = min((i + 1) * batch_size, total_codes)
            batch_codes = code_list[start_index:end_index]

            logger.info(f"Processing batch {i + 1}/{num_batches}: codes {start_index + 1} to {end_index}")

            try:
                # 获取当前批次的数据
                df = self.ts_api.get_daily_prices_cn(batch_codes, start_date, end_date)

                # 写入数据库
                if not df.empty:
                    self.repo.insert(df, 'daily_prices_realtime_cn')
                    logger.info(f"Successfully inserted {len(df)} rows for batch {i + 1}")
                else:
                    logger.warning(f"No data returned for batch {i + 1}")
            except Exception as e:
                logger.error(f"Error processing batch {i + 1}: {e}")

        logger.info("All batches processed successfully.")

    def update_moving_averages(self, region):
        df = self.repo.calculate_moving_averages_batch(region)
        df['region'] = region
        print(f"Updating {len(df)} rows of moving averages.")

        if not df.empty:
            self.repo.delete_ma(region)
            self.repo.insert(df, "moving_averages")


if __name__ == '__main__':
    daily_prices_api = DailyPricesAPI()
    daily_prices_api.update_daily_price_realtime_cn()
    #daily_prices_api.update_moving_averages('cn')




