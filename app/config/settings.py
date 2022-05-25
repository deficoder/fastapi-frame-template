import logging, sys, os

from .log_handler import InterceptHandler

from loguru import logger
from pydantic import BaseSettings

from starlette.config import Config


class Settings(BaseSettings):
    DEBUG:                  bool = False

    TITLE:                  str = ''
    VERSION:                str = ''
    HOST_NAME:              str = ''
    PORT:                   int = None
    API_PREFIX:             str = ''

    REDIS_HOST:             str = ''
    REDIS_PASSWORD:         str = ''
    REDIS_DB:               int = None
    REDIS_PORT:             int = None

    CELERY_BROKER:          str = ''
    CELERY_BACKEND:         str = ''
    CELERY_INTERVAL:        int = 0
    
def load_config():
    envPath = os.getenv('ENV_FILEPATH', '.env')
    if not envPath or not os.path.exists(envPath):
        sys.exit('Not find .env file')

    config = Config(envPath)
    logger.log(logging.INFO, 'ENV_FILEPATH:{}'.format(envPath))

    SETTINGS                = Settings()
    SETTINGS.DEBUG          = config('DEBUG', cast=bool, default=False)
    SETTINGS.TITLE          = config('TITLE')
    SETTINGS.VERSION        = config('VERSION')
    SETTINGS.HOST_NAME      = config('HOST_NAME', default='0.0.0.0')
    SETTINGS.PORT           = config('PORT', cast=int)
    SETTINGS.API_PREFIX     = config('API_PREFIX')

    SETTINGS.REDIS_HOST     = config('REDIS_HOST')
    SETTINGS.REDIS_PASSWORD = config('REDIS_PASSWORD')
    SETTINGS.REDIS_DB       = config('REDIS_DB', cast=int)
    SETTINGS.REDIS_PORT     = config('REDIS_PORT', cast=int)

    SETTINGS.CELERY_BROKER  = config('CELERY_BROKER', default=f'redis://:{SETTINGS.REDIS_PASSWORD}@{SETTINGS.REDIS_HOST}:{SETTINGS.REDIS_PORT}/{SETTINGS.REDIS_DB}')
    SETTINGS.CELERY_BACKEND = config('CELERY_BACKEND', default=f'redis://:{SETTINGS.REDIS_PASSWORD}@{SETTINGS.REDIS_HOST}:{SETTINGS.REDIS_PORT}/{SETTINGS.REDIS_DB}')
    SETTINGS.CELERY_INTERVAL= config('CELERY_INTERVAL', cast=int)
    
    LOGGING_LEVEL = logging.DEBUG if SETTINGS.DEBUG else logging.INFO
    logging.getLogger().handlers = [InterceptHandler(level=LOGGING_LEVEL)]
    for logger_name in ['uvicorn.asgi', 'uvicorn.access']:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]
    logger.configure(handlers=[{'sink': sys.stderr, 'level': LOGGING_LEVEL}])

    return SETTINGS, LOGGING_LEVEL

SETTINGS, LOGGING_LEVEL = load_config()