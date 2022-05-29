from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware

from apis import router

from config.settings import SETTINGS, LOGGING_LEVEL
from config.middleware import CertifiedMiddleware

from loguru import logger

def startup_event():
    logger.log(LOGGING_LEVEL, 'Startup {}'.format(SETTINGS.TITLE))

def shutdown_event():
    logger.log(LOGGING_LEVEL, 'Shutdown {}'.format(SETTINGS.TITLE))

def get_application(title, debug, version, api_prefix) -> FastAPI:
    application = FastAPI(title=title, debug=debug, version=version)

    # add_middleware
    application.add_middleware(CertifiedMiddleware)
    application.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
    
    # add_event_handler
    application.add_event_handler('startup', startup_event)
    application.add_event_handler('shutdown', shutdown_event)

    # include apis router
    logger.log(LOGGING_LEVEL, f'API Prefix {api_prefix}')
    application.include_router(router, prefix=api_prefix)

    return application

app = get_application(title=SETTINGS.TITLE, debug=SETTINGS.DEBUG, version=SETTINGS.VERSION, api_prefix=SETTINGS.API_PREFIX)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host=SETTINGS.HOST_NAME, port=SETTINGS.PORT, reload=True, debug=SETTINGS.DEBUG)
