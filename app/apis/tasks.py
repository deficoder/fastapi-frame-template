from fastapi import APIRouter
from fastapi.responses import JSONResponse

from starlette import status

from tasks.backend import remote_task

router = APIRouter()

@router.get('')
def test_task():
    task = remote_task.apply_async()
    return JSONResponse(status_code=status.HTTP_200_OK, content={'code':0, 'msg': 'success', 'task':task.id})

