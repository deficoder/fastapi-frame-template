import os
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Query, Form
from fastapi.responses import FileResponse, JSONResponse
from starlette.background import BackgroundTask
from typing import List

from loguru import logger

import pandas as pd

from config.settings import LOGGING_LEVEL, SETTINGS
from tasks.backend import youtube_download_task
from utils.file_tools import format_file_size

router = APIRouter()

@router.post('/subtitle/csv_to_text', summary='Upload csv subtitle and converter to .txt format')
def subtitle_csv_to_text(upfile: UploadFile = File(...)):
    now = datetime.timestamp(datetime.now())
    logger.log(LOGGING_LEVEL, f'Receive file {upfile.filename}')

    targetName = str(upfile.filename).replace('csv', 'txt')
    targetFile = os.path.join(SETTINGS.PLAYLIST_PATH, targetName)
    tmpPath = os.path.join('/tmp', f'subtitle_{now}.csv')

    with open(tmpPath, 'wb') as tmpf:
        tmpf.write(upfile.file.read())
        tmpf.close()

    df = pd.read_csv(tmpPath, sep=';')

    rows = []
    for r in df.iterrows():
        data = r[1]

        text = '{}\n{}\n'.format(data['Number'], str(data['Text']).replace('<i>', '').replace('</i>', '').replace('\n', ' [**] '))
        rows.append(text)

    with open(targetFile, 'w') as tf:
        tf.writelines('\n'.join(rows))
    
    res = FileResponse(path=targetFile, filename=targetName, media_type='application/octet-stream', background=BackgroundTask(lambda: os.remove(tmpPath)))
    res.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'

    return res

@router.post('/video/youtube_dl')
async def youtube_dl(video_urls: str = Form(...), audio_format: str = Form('mp3')):
    res = []
    for url in video_urls.split(','):
        task = youtube_download_task.apply_async(args=(url, audio_format))
        res.append(dict(video_url=url, task_id=task.id))
    
    return JSONResponse(res)

@router.get('/playlist')
def get_playlist():
    res = []
    for li in os.listdir(SETTINGS.PLAYLIST_PATH):
        path = os.path.join(SETTINGS.PLAYLIST_PATH, li)
        if os.path.isfile(path):
            filestat = os.stat(path)
            if filestat.st_size == 0:
                continue
            
            res.append(dict(filename=li, filesize=format_file_size(filestat.st_size)))

    return JSONResponse(res)

@router.get('/playlist/download')
def playlist_download(filename: str = Query(...)):
    filepath = os.path.join(SETTINGS.PLAYLIST_PATH, filename)

    res = FileResponse(path=filepath, filename=filename, media_type='application/octet-stream')
    res.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'

    return res