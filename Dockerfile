# Use an official Python runtime as a base image
FROM python:3.9-slim

LABEL maintainer="jspawar80@gmail.com"

ENV DOCKER=true

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY pyproject.toml poetry.lock /app/

# Install Poetry
RUN pip install poetry

# Install project dependencies
RUN poetry install --no-root --no-dev

# Copy the entire application to the container
COPY . /app

# Expose the port that FastAPI runs on
EXPOSE 8000
