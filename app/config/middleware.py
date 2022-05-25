from loguru import logger

from fastapi.responses import JSONResponse

from starlette.middleware.base import BaseHTTPMiddleware
from starlette import status

from .settings import LOGGING_LEVEL

class CertifiedMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Do something
        # source_ip = request.headers.get('source_ip')
        # if source_ip not in ['1.1.1.1']:
        #     return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'code':-1, 'msg': 'Access Not Allowed'})

        return await call_next(request)