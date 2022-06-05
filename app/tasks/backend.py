import os

from loguru import logger
from config.settings import LOGGING_LEVEL, SETTINGS

from celery import Celery

from kombu import Exchange, Queue

# Celery 
app = Celery('tasks', broker=SETTINGS.CELERY_BROKER, backend=SETTINGS.CELERY_BACKEND)
app.conf.update(result_expires=60, task_serializer='json', accept_content=['json'], result_serializer='json', timezone='Asia/Shanghai', enable_utc=False)

app.conf.task_queues = (
    Queue('default', Exchange('default', type='direct'), routing_key='default'),
)
app.conf.task_default_queue = 'default'
app.conf.task_default_exchange_type = 'direct'
app.conf.task_default_routing_key = 'default'

app.autodiscover_tasks()

@app.on_after_configure.connect
def add_periodic(**kargs):
    app.add_periodic_task(SETTINGS.CELERY_INTERVAL, periodic_task.s(), name='exec periodic task every {}'.format(SETTINGS.CELERY_INTERVAL))

@app.task(name='periodic_task')
def periodic_task():
    logger.log(LOGGING_LEVEL, 'Hello periodic_task')

@app.task(name='remote_task')
def remote_task():
    logger.log(LOGGING_LEVEL, 'remote task')

@app.task(name='youtube_download_task')
def youtube_download_task(vedio_url, audio_format = 'mp3'):
    vedio_id = vedio_url.split('&')[0].replace('https://www.youtube.com/watch?v=', '')
    logger.log(LOGGING_LEVEL, f'vedio_id {vedio_id} {audio_format}')
    
    pathDir = os.path.join(SETTINGS.PLAYLIST_PATH, vedio_id)

    if os.path.exists(pathDir) and os.path.getsize(pathDir) > 0:
        return f'Video {pathDir} is downloading, please wait...'

    # mkdir pathDir and exec youtube download
    os.system(f"mkdir -p {pathDir} && youtube-dl --extract-audio --audio-format {audio_format} --write-sub -o {pathDir}/'%(title)s.{vedio_id}.%(ext)s' -k {vedio_url} --restrict-filenames")
    
    # save .vtt, .mp3, .mp4 into playlist dir
    videoNames = []
    
    fileList = os.listdir(pathDir)
    if not fileList:
        fileList = []

    for file in fileList:
        videoName = file.split('.')[0]
        videoNames.append(videoName)
        
        fileName = os.path.join(SETTINGS.PLAYLIST_PATH, videoName)

        # force move to playlist
        cmd = 'mv -f {} {}'.format(os.path.join(pathDir, file), fileName)
        
        if file.endswith('.vtt'):
            os.system(f'{cmd}.vtt')

        elif file.endswith(f'{vedio_id}.{audio_format}'):
            os.system(f'{cmd}.{audio_format}')

        elif file.endswith(f'{vedio_id}.mp4'):
            os.system(f'{cmd}.mp4')
        
    # clear tmp dir
    os.system(f'rm -rf {pathDir}')
    return ','.join(videoNames)