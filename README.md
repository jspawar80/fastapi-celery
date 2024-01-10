# FastAPI with Celery

> Minimal example utilizing FastAPI and Celery with RabbitMQ for task queue, Redis for Celery backend and flower for monitoring the Celery tasks.

## Application Architecture


1. FastAPI Application at the center, as it's the entry point for requests.
2. RabbitMQ connected to FastAPI, representing the task queue.
3. Celery Workers, showing their connection to RabbitMQ for receiving tasks.
4. Redis, linked to Celery, depicting its role as the backend for task results and state management.
5. Flower, also connected to Celery, for monitoring tasks and workers.

- FastAPI handles incoming HTTP requests, triggers background tasks, and provides endpoints to interact with the application's functionalities.
- FastAPI pushes tasks into the RabbitMQ queue. Celery workers subscribe to this queue, pulling tasks for execution as they become available.
- Workers receive tasks from RabbitMQ, execute them independently or in parallel, and update task states. They push task results and status updates back to the backend.
- Celery uses Redis for task result storage, caching, and managing the state of tasks. It stores task outputs, states, and other transient data, providing a fast and persistent storage solution.
- Flower connects to the Celery, allowing administrators or developers to monitor task progress, worker statuses, and overall system health through an intuitive web interface.

## Application code explanation.

This FastAPI application integrates with Celery, a task queue system, to handle asynchronous tasks efficiently. The code defines two main endpoints. The first endpoint (/{word}) triggers a background task when accessed via a GET request. It sends the provided word as a parameter to a Celery task and returns the unique ID of the task. The second endpoint (/process/{task_id}) retrieves the status and result of a specific task based on its ID. It constructs a response containing the task's ID, its current status (such as "processing" or "completed"), any encountered errors, and the task's result if it has finished successfully.

### This FastAPI code sets up two endpoints:

1. Trigger Task Endpoint (/{word}): Receives a word via a GET request, sends it as a background Celery task, and returns the task's ID.

2. Task Result Endpoint (/process/{task_id}): Retrieves the status and result of a task based on its ID, presenting the task's ID, status, any errors encountered, and the result (if successful). The tasks run asynchronously using Celery for background processing.

- A Celery worker is a process or a set of processes responsible for executing tasks asynchronously within a Celery-based distributed task queue system. These workers pull tasks from the message broker, execute them, and manage the task lifecycle, including tracking their progress, updating status, and handling results.
- The celery_app.py file initializes the Celery application differently based on whether it's running with or without Docker. It configures the Celery app with specific backend and broker settings.
- Without Docker, it uses Redis as the backend for storing task results and RabbitMQ as the message broker for handling task queues and message passing . It also sets up a task route for a specific task (app.worker.celery_worker.test_celery) to a queue named test-queue.
- Moving on to celery_worker.py, it contains the Celery task definition test_celery(word: str). This task simulates work by running a loop that sleeps for one second in each iteration. During this loop, it updates the task's state to 'PROGRESS' and includes metadata indicating the progress percentage (increments of 10 from 10% to 100%). Finally, it returns a string with the word provided in the argument.
- Using Redis as a backend for Celery involves utilizing Redis as the storage mechanism for Celery's task results and other operational data. Redis serves as a fast, in-memory data structure store that can be used for various purposes, including task result storage in Celery.
- RabbitMQ (Message Broker): Facilitates communication between the FastAPI application and Celery workers. It ensures reliable message delivery, queues incoming tasks, and distributes them among workers for processing. RabbitMQ acts as a middleman for task distribution, ensuring tasks are executed asynchronously without overloading the application.
- Redis (Backend): Serves as a fast and persistent storage solution for Celery. Redis stores task results, manages task states, and caches frequently accessed data. It allows Celery workers to update task statuses, store outputs, and retrieve necessary information efficiently, contributing to the reliability and performance of task execution within the system.


##  Automatic scaling of your Kubernetes deployments

I'm using HPA configurations based on CPU utilization.

This HPA configuration specifies that the celery-worker Deployment should have a minimum of 1 replicas and a maximum of 10. 
These HPAs are set to scale the respective deployments between 1 and 10 replicas based on CPU utilization.

To enable automatic scaling of your Kubernetes deployments, including scaling down to zero and up from zero based on incoming traffic, you can utilize Kubernetes Horizontal Pod Autoscaler (HPA) in conjunction with a serverless framework like KEDA (Kubernetes-based Event-Driven Autoscaling).
KEDA can extend the functionality of Kubernetes HPA to support scaling to and from zero, which is not possible with the standard HPA. KEDA works by activating and deactivating Kubernetes deployments, allowing them to scale from zero to N instances and back to zero.


## challenges encountered and the corresponding approaches to address them:

Challenge: Integration between FastAPI and Celery.
Approach: We structured the code to enable FastAPI to trigger Celery tasks asynchronously. By leveraging Celery's ability to execute tasks asynchronously, we designed the FastAPI endpoints to initiate tasks via Celery, allowing the application to handle long-running operations without blocking the main thread.

Challenge: Orchestrating multiple services like RabbitMQ, Redis, FastAPI, and Celery using Docker and Docker Compose to ensure seamless communication between these components.
Approach: We utilized Docker and Docker Compose to containerize and manage services. Each service, such as RabbitMQ, Redis, FastAPI, and Celery, was containerized, allowing easy setup, isolation, same network, and reproducibility across different environments.

Challenge: Managing configuration settings, such as connection details for RabbitMQ, Redis, and Celery within the application.
Approach: We used environment variables to parameterize configurations, making the application more flexible. This approach allows modifying configurations without changing the code directly, enabling easier deployment across various environments.

Challenge: Maintaining an efficient development workflow, ensuring code quality, and testing the FastAPI and Celery integration.

### troubleshooting a Kubernetes deployment:

Problem: Celery tasks dispatched from FastAPI were stuck in a 'PENDING' state, and Flower UI wasn't showing the Celery workers.
Approach:
1. Ensured proper internal networking within Kubernetes, allowing communication between FastAPI, Celery workers, RabbitMQ, and Redis.
2. Verified RabbitMQ and Redis service configurations in Kubernetes, ensuring correct environmental variables and network access for FastAPI and Celery workers.
Advised checking Kubernetes network policies and suggested increasing resource allocation if necessary.

Challenge: Required accurate Kubernetes configurations for deploying multiple interdependent services.
Solution: Crafted and applied detailed Kubernetes YAML configurations for deployments and services, including NodePort services for external access and environment variables for inter-service communication.


### Integration between FastAPI and Celery 

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

### Run on kubernetes.
 1. Clone the repository.
```
git clone https://github.com/jspawar80/fastapi-celery.git
``
2. Deployment on kubernetes.
```
cd fastapi-celery/
kubectl apply -f K8s/
```
 
