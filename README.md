# FastAPI with Celery

> Minimal example utilizing FastAPI and Celery with RabbitMQ for task queue, Redis for Celery backend and flower for monitoring the Celery tasks.

## Application Architecture


1. FastAPI Application at the center, as it's the entry point for requests.
2. RabbitMQ connected to FastAPI, representing the task queue.
3. Celery Workers, showing their connection to RabbitMQ for receiving tasks.
4. Redis, linked to Celery, depicting its role as the backend for task results and state management.
5. Flower, also connected to Celery, for monitoring tasks and workers.

This diagram shows the flow of tasks from the FastAPI application, through RabbitMQ and Celery, with state management in Redis, and monitoring through Flower

##  Automatic scaling of your Kubernetes deployments

I'm using HPA configurations based on CPU utilization.

This HPA configuration specifies that the celery-worker Deployment should have a minimum of 1 replicas and a maximum of 10. 
These HPAs are set to scale the respective deployments between 1 and 10 replicas based on CPU utilization.

To enable automatic scaling of your Kubernetes deployments, including scaling down to zero and up from zero based on incoming traffic, you can utilize Kubernetes Horizontal Pod Autoscaler (HPA) in conjunction with a serverless framework like KEDA (Kubernetes-based Event-Driven Autoscaling).
KEDA can extend the functionality of Kubernetes HPA to support scaling to and from zero, which is not possible with the standard HPA. KEDA works by activating and deactivating Kubernetes deployments, allowing them to scale from zero to N instances and back to zero.


## Requirements

- Docker
  - [docker-compose](https://docs.docker.com/compose/install/)

## Run example

1. Run command ```docker-compose up```to start up the RabbitMQ, Redis, flower and our application/worker instances.
2. Navigate to the [http://localhost:8000/docs](http://localhost:8000/docs) and execute test API call. You can monitor the execution of the celery tasks in the console logs or navigate to the flower monitoring app at [http://localhost:5555](http://localhost:5555) (username: user, password: test).

## Run application/worker without Docker?

### Requirements/dependencies

- Python >= 3.7
  - [poetry](https://python-poetry.org/docs/#installation)
- RabbitMQ instance
- Redis instance

> The RabbitMQ, Redis and flower services can be started with ```docker-compose -f docker-compose-services.yml up```

### Install dependencies

Execute the following command: ```poetry install --dev```

### Run FastAPI app and Celery worker app

1. Start the FastAPI web application with ```poetry run hypercorn app/main:app --reload```.
2. Start the celery worker with command ```poetry run celery worker -A app.worker.celery_worker -l info -Q test-queue -c 1```
3. Navigate to the [http://localhost:8000/docs](http://localhost:8000/docs) and execute test API call. You can monitor the execution of the celery tasks in the console logs or navigate to the flower monitoring app at [http://localhost:5555](http://localhost:5555) (username: user, password: test).
