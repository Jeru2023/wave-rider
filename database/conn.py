from sqlalchemy import create_engine
import configparser as cp
import os
from tools import utils
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Connection:
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
        enable_sql_logging = config.getboolean('DB', 'enable_sql_logging')

        if enable_sql_logging:
            # enable SQLAlchemy sql logging
            sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
            sqlalchemy_logger.setLevel(logging.INFO)

        return create_engine(
            'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database),
            pool_size=20,
            max_overflow=50,
            pool_recycle=30
        )

    def get_connection(self):
        return self.engine

