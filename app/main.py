import os
import logging
from threading import Thread

from fastapi import FastAPI, BackgroundTasks
from starlette.status import HTTP_200_OK
from worker.celery_app import celery_app
from starlette.responses import JSONResponse
from celery import states
from base_objects import TaskResult

log = logging.getLogger(__name__)


app = FastAPI()

def celery_on_message(body):
    log.warn(body)

def background_on_message(task):
    log.warn(task.get(on_message=celery_on_message, propagate=False))


@app.get("/{word}")
async def root(word: str, background_task: BackgroundTasks):

    # set correct task name based on the way you run the example
    if os.getenv('DOCKER') is not None:
        task_name = "app.worker.celery_worker.test_celery"
    else:
        task_name = "app.worker.celery_worker.test_celery"

    task = celery_app.send_task(task_name, args=[word])
    background_task.add_task(background_on_message, task)

    return {"process_id": task.id}

@app.get("/process/{task_id}")
async def get_task_result(task_id: str) -> JSONResponse:
    result = celery_app.AsyncResult(task_id)

    output = TaskResult(
        id=task_id,
        status=result.state,
        error=str(result.info) if result.failed() else None,
        result=result.get() if result.state == states.SUCCESS else None
    )

    return JSONResponse(
        status_code=HTTP_200_OK,
        content=output.dict()
    )
