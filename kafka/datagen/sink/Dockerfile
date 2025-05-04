FROM bitnami/kafka:3.5

ADD connect-standalone.properties connect-minio-sink.properties /opt/bitnami/kafka

RUN mkdir /opt/bitnami/kafka/filesink

ENTRYPOINT ["sh", "-c", "/opt/bitnami/kafka/bin/connect-standalone.sh /opt/bitnami/kafka/connect-standalone.properties /opt/bitnami/kafka/connect-minio-sink.properties"]