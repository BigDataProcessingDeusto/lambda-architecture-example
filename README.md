# Processing Large Volumes of Data - Lambda architecture example

This is an example of a Lambda architecture. You can find more information at course materials.

## Procedure

To start services: 

```
$ ./docker-compose up
```

To stop services:

```
$ ./docker-compose down
```

Minio is accesible at [http://localhost:9000](http://localhost:9000) (user: `minio-root-user`, password: `minio-root-password`).

Kafka topics can be consumed using following commands:

```
$ sh -c "cd kafka && docker compose exec -ti kafka-server /opt/bitnami/kafka/bin/kafka-console-consumer.sh --topic pizza-orders --bootstrap-server localhost:9092"
$ sh -c "cd kafka && docker compose exec -ti kafka-server /opt/bitnami/kafka/bin/kafka-console-consumer.sh --topic pizza-live-stats --bootstrap-server localhost:9092"
```

Spark is accesible at [http://localhost:8081](http://localhost:8081).

Airflow is accesible at [http://localhost:8080](http://localhost:8080) (user: `airflow`, password: `airflow`).