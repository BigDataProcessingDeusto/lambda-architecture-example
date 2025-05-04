FROM bitnami/kafka:3.5

ADD libs/* /opt/bitnami/kafka/libs
ADD pizza-cancelled-orders-source.properties pizza-orders-source.properties connect-standalone.properties /opt/bitnami/kafka

RUN mkdir /opt/bitnami/kafka/filesink

ENTRYPOINT ["sh", "-c", "CLASSPATH=/opt/bitnami/kafka/connect-file-3.5.2.jar /opt/bitnami/kafka/bin/connect-standalone.sh /opt/bitnami/kafka/connect-standalone.properties /opt/bitnami/kafka/pizza-orders-source.properties /opt/bitnami/kafka/pizza-cancelled-orders-source.properties"]
