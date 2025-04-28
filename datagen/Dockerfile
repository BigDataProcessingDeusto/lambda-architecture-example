FROM bitnami/kafka:3.5

ADD libs/* /opt/bitnami/kafka/libs
ADD pizza-cancelled-orders-source.properties pizza-orders-source.properties connect-standalone.properties /opt/bitnami/kafka

ENTRYPOINT ["sh", "-c", "/opt/bitnami/kafka/bin/connect-standalone.sh /opt/bitnami/kafka/connect-standalone.properties /opt/bitnami/kafka/pizza-orders-source.properties /opt/bitnami/kafka/pizza-cancelled-orders-source.properties"]