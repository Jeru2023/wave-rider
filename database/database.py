from sqlalchemy import create_engine
import configparser as cp
import os
from tools import utils


class Database:
    def __init__(self):
        self.engine = self._create_engine()

    @staticmethod
    def _create_engine():
        config = cp.ConfigParser()
        config_path = os.path.join(utils.get_root_path(), 'config', 'stock.config')
        config.read(config_path, encoding='utf-8-sig')

        user = config.get('DB', 'user')
        password = config.get('DB', 'password')
        host = config.get('DB', 'host')
        port = config.get('DB', 'port')
        database = config.get('DB', 'database')

        return create_engine(
            'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database),
            pool_size=20,
            max_overflow=50,
            pool_recycle=30
        )

    def get_connection(self):
        return self.engine

