<h3 align="center">Fastapi Frame Template!</h3>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-14354C?logo=Python&logoColor=white">
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-20232a?logo=fastapi&logoColor=white">
  <img alt="Celery" src="https://img.shields.io/badge/Celery-9CCF1C?logo=celery&logoColor=white">
  <img alt="Docker" src="https://img.shields.io/badge/Docker-46a2f1?logo=docker&logoColor=white">
  <br>
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira%20Code&center=true&width=440&height=45&color=0F95F7FC&vCenter=true&size=22&lines=Quickly+build+Python+services+based+on+FastAPI">
  <br>
  <img align="center" width="160" height="120" src="https://media.giphy.com/media/l378zf8b3gdqqVjIQ/giphy.gif">
</p>

```yaml
uvicorn main:app --host 0.0.0.0 --port 8001 --reload

celery -A tasks.backend beat --loglevel=info
celery -A tasks.backend woker --loglevel=info
celery -A tasks.backend flower --address=0.0.0.0 --port=8300 --loglevel=info
```