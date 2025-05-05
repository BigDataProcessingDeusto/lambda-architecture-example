FROM apache/airflow:3.0.0

USER root
# RUN apt update && apt install -y procps openjdk-8-jdk
RUN curl https://repo.huaweicloud.com/java/jdk/8u202-b08/jdk-8u202-linux-x64.tar.gz -o /tmp/jdk-8u202-linux-x64.tar.gz
RUN mkdir -p /opt/java
RUN tar -xvzf /tmp/jdk-8u202-linux-x64.tar.gz -C /opt/java
#ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
ENV JAVA_HOME /opt/java/jdk1.8.0_202
RUN export JAVA_HOME

USER airflow
#ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
ENV JAVA_HOME /opt/java/jdk1.8.0_202
RUN export JAVA_HOME

RUN pip install "apache-airflow==${AIRFLOW_VERSION}" --no-cache-dir apache-airflow-providers-apache-spark apache-airflow[amazon]