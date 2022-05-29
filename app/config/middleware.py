from starlette.middleware.base import BaseHTTPMiddleware

class CertifiedMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Do something
        # source_ip = request.headers.get('source_ip')
        # if source_ip not in ['1.1.1.1']:
        #     return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'code':-1, 'msg': 'Access Not Allowed'})

        response = await call_next(request)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = '*' #'POST, PUT, GET, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] =  '*' #'Authorization, Content-Type, Access-Control-Expose-Headers, Content-Disposition'
        return response