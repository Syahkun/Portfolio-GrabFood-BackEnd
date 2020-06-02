import configparser
from datetime import timedelta

cfg = configparser.ConfigParser()
cfg.read('config.cfg')


class Config():
    SQLALCHEMY_DATABASE_URI = '%s+%s://%s:%s@%s:%s/%s' % (
        cfg['database']['default_connection'],
        cfg['mysql']['driver'],
        cfg['mysql']['user'],
        cfg['mysql']['kata_kunci'],
        cfg['mysql']['host'],
        cfg['mysql']['port'],
        cfg['mysql']['db']

    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = cfg['jwt']['secret_key']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)


class DevelopmentConfig(Config):
    APP_DEBUG = True
    DEBUG = True
    MAX_BYTES = 10000


class ProductionConfig(Config):
    APP_DEBUG = True
    DEBUG = True
    MAX_BYTES = 10000
