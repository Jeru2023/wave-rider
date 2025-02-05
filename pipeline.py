from api.daily_prices_api import DailyPricesAPI


class Pipeline:
    def __init__(self):
        self.dp_api = DailyPricesAPI()

    def run(self):
        pass
