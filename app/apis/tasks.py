import os
from datetime import datetime
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask

from loguru import logger

import pandas as pd

from config.settings import LOGGING_LEVEL

router = APIRouter()

@router.post('/subtitle/csv_to_text', summary='Upload csv subtitle and converter to .txt format')
def subtitle_csv_to_text(upfile: UploadFile = File(...)):
    logger.log(LOGGING_LEVEL, f'Receive file {upfile.filename}')

    targetName = str(upfile.filename).replace('csv', 'txt')
    tmpPath = '/tmp/subtitle_{}.csv'.format(datetime.timestamp(datetime.now()))

    with open(tmpPath, 'wb') as tmpf:
        tmpf.write(upfile.file.read())
        tmpf.close()

    df = pd.read_csv(tmpPath, sep=';')

    rows = []
    for r in df.iterrows():
        data = r[1]

        text = '{}\n{}\n'.format(data['Number'], str(data['Text']).replace('<i>', '').replace('</i>', '').replace('\n', ' [**] '))
        rows.append(text)

    with open(f'/tmp/{targetName}', 'w') as tf:
        tf.writelines('\n'.join(rows))
    
    res = FileResponse(path=f'/tmp/{targetName}', filename=targetName, media_type='application/octet-stream', background=BackgroundTask(lambda: os.remove(f'/tmp/{targetName}')))
    res.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'

    return res
