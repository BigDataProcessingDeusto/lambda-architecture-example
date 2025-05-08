#!/bin/bash

TIMEOUT=30
COUNTER=0

if [ -z "$1" ]; then
  echo "Usage: $0 [up|down]"
  exit 1
fi

if command -v docker-compose &> /dev/null; then
  echo "Using legacy docker-compose"
  DOCKER_COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
  echo "Using modern docker compose"
  DOCKER_COMPOSE_CMD="docker compose"
else
  echo "Neither docker-compose nor docker compose is available."
  exit 1
fi

down() {
  echo "Stopping services..."

    WORKDIR=airflow
    SERVICE=Airflow
    stop_service

    WORKDIR=spark
    SERVICE=Spark
    stop_service

    WORKDIR=kafka
    SERVICE=Kafka
    stop_service

    WORKDIR=minio
    SERVICE=Minio
    stop_service
}

start_service() {
    echo "Starting $SERVICE..."
    (
        cd $WORKDIR && $DOCKER_COMPOSE_CMD up -d --build
    )
    while ! nc -z localhost $PORT; do
        sleep 1
        ((COUNTER++))
        if [ $COUNTER -ge $TIMEOUT ]; then
            echo "Timeout: $SERVICE did not start within $TIMEOUT seconds."
            exit 1
        fi
    done
    echo "$SERVICE is now running on port $PORT."
}

stop_service() {
    echo "Stopping $SERVICE..."
    (
      cd $WORKDIR && $DOCKER_COMPOSE_CMD down
    )
}

case "$1" in
  up)
    down
    echo "Starting lambda architecture example"
    
    WORKDIR=minio
    SERVICE=Minio
    PORT=9000
    start_service

    WORKDIR=kafka
    SERVICE=Kafka
    PORT=9092
    start_service

    WORKDIR=spark
    SERVICE=Spark
    PORT=8081
    start_service

    echo "Starting Airflow..."
    (
      cd airflow && mkdir -p config && mkdir -p logs && mkdir -p plugins && 
      $DOCKER_COMPOSE_CMD run airflow-cli airflow config list && $DOCKER_COMPOSE_CMD up airflow-init && 
      $DOCKER_COMPOSE_CMD up -d --build 
    )
    while ! nc -z localhost 8080; do
        sleep 1
        ((COUNTER++))
        if [ $COUNTER -ge $TIMEOUT ]; then
            echo "Timeout: Airflow server did not start within $TIMEOUT seconds."
            exit 1
        fi
    done
    echo "Airflow server is now running on port 8080."
    ;;
  down)
    echo "You selected DOWN. Stopping services..."
    
    down
    
    ;;
  *)
    echo "Invalid option: $1"
    echo "Usage: $0 [up|down]"
    exit 1
    ;;
esac