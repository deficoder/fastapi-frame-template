from fastapi import APIRouter
from fastapi.responses import JSONResponse

from . import tasks

router = APIRouter()

@router.get('/health')
def health():
    return {'code':0, 'msg':'success'}

router.include_router(tasks.router, prefix='/tasks')