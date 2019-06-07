FROM ubuntu:16.04

RUN apt-get update && apt-get install -y --no-install-recommends \
		bzip2 \
		unzip \
		xz-utils \
		vim \
		net-tools


# Default to UTF-8 file.encoding
ENV LANG C.UTF-8
ENV JOB_ID 0
ENV SFTP_HOSTNAME ec2-3-17-129-179.us-east-2.compute.amazonaws.com
ENV SFTP_USERNAME nifi-test
ENV SFTP_PASSWORD nifi-test
ENV SFTP_REMOTE_PATH /home/nifi-test/random_data
ENV HADOOP_CONFIGURATION_RESOURCES /opt/nifi/nifi-current/hdfs-site.xml,/opt/nifi/nifi-current/core-site.xml
ENV HADOOP_DIRECTORY /nifi-test1
ENV PUTSQLGET_SQL_STATEMENT 'insert into DataLoadFile values(${JOB_ID}, '\${filename}', 0);'
ENV PUTSQLPUT_SQL_STATEMENT 'insert into DataLoadFile values(${JOB_ID}, '\${filename}', 1) on duplicate key update transferred = 1;'
ENV SQL_HOST ec2-3-14-65-63.us-east-2.compute.amazonaws.com
ENV SQL_PORT 30868
ENV SQL_USER root
ENV SQL_PASS password
ENV SQL_DB CoutureConsoleDB






RUN apt-get install -y default-jre default-jdk

ARG UID=1000
ARG GID=1000
ARG NIFI_VERSION=1.9.0
ARG BASE_URL=https://archive.apache.org/dist
ARG MIRROR_BASE_URL=${MIRROR_BASE_URL:-${BASE_URL}}
ARG NIFI_BINARY_PATH=${NIFI_BINARY_PATH:-/nifi/${NIFI_VERSION}/nifi-${NIFI_VERSION}-bin.zip}
ARG NIFI_TOOLKIT_BINARY_PATH=${NIFI_TOOLKIT_BINARY_PATH:-/nifi/${NIFI_VERSION}/nifi-toolkit-${NIFI_VERSION}-bin.zip}

ENV NIFI_BASE_DIR=/opt/nifi
ENV NIFI_HOME ${NIFI_BASE_DIR}/nifi-current
ENV NIFI_TOOLKIT_HOME ${NIFI_BASE_DIR}/nifi-toolkit-current

ENV NIFI_PID_DIR=${NIFI_HOME}/run
ENV NIFI_LOG_DIR=${NIFI_HOME}/logs

ADD sh/ ${NIFI_BASE_DIR}/scripts/

# Setup NiFi user and create necessary directories
RUN groupadd -g ${GID} nifi || groupmod -n nifi `getent group ${GID} | cut -d: -f1` \
    && useradd --shell /bin/bash -u ${UID} -g ${GID} -m nifi \
    && mkdir -p ${NIFI_BASE_DIR} \
    && chown -R nifi:nifi ${NIFI_BASE_DIR} \
    && apt-get update \
    && apt-get install -y jq xmlstarlet procps

#standard apt packages
RUN apt-get install -y apt-transport-https apt-utils software-properties-common curl

#--------------install required dependencies--------------
RUN apt-get install -y build-essential libssl-dev libffi-dev libsasl2-dev libldap2-dev libxi-dev libmysqlclient-dev

#----------install python3 and development tools----------
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get update -y && apt-get install -y python3.6
RUN apt-get install python3.6-dev python3-pip python-dev -y
RUN python3.6 -m pip install --upgrade setuptools pip wheel


#------install python packages from requirements.txt------
COPY requirements.txt ./
RUN python3.6 -m pip install -r ./requirements.txt

USER nifi

# Download, validate, and expand Apache NiFi Toolkit binary.
RUN curl -fSL ${MIRROR_BASE_URL}/${NIFI_TOOLKIT_BINARY_PATH} -o ${NIFI_BASE_DIR}/nifi-toolkit-${NIFI_VERSION}-bin.zip \
    && echo "$(curl ${BASE_URL}/${NIFI_TOOLKIT_BINARY_PATH}.sha256) *${NIFI_BASE_DIR}/nifi-toolkit-${NIFI_VERSION}-bin.zip" | sha256sum -c - \
    && unzip ${NIFI_BASE_DIR}/nifi-toolkit-${NIFI_VERSION}-bin.zip -d ${NIFI_BASE_DIR} \
    && rm ${NIFI_BASE_DIR}/nifi-toolkit-${NIFI_VERSION}-bin.zip \
    && mv ${NIFI_BASE_DIR}/nifi-toolkit-${NIFI_VERSION} ${NIFI_TOOLKIT_HOME} \
    && ln -s ${NIFI_TOOLKIT_HOME} ${NIFI_BASE_DIR}/nifi-toolkit-${NIFI_VERSION}

# Download, validate, and expand Apache NiFi binary.
RUN curl -fSL ${MIRROR_BASE_URL}/${NIFI_BINARY_PATH} -o ${NIFI_BASE_DIR}/nifi-${NIFI_VERSION}-bin.zip \
    && echo "$(curl ${BASE_URL}/${NIFI_BINARY_PATH}.sha256) *${NIFI_BASE_DIR}/nifi-${NIFI_VERSION}-bin.zip" | sha256sum -c - \
    && unzip ${NIFI_BASE_DIR}/nifi-${NIFI_VERSION}-bin.zip -d ${NIFI_BASE_DIR} \
    && rm ${NIFI_BASE_DIR}/nifi-${NIFI_VERSION}-bin.zip \
    && mv ${NIFI_BASE_DIR}/nifi-${NIFI_VERSION} ${NIFI_HOME} \
    && mkdir -p ${NIFI_HOME}/conf \
    && mkdir -p ${NIFI_HOME}/database_repository \
    && mkdir -p ${NIFI_HOME}/flowfile_repository \
    && mkdir -p ${NIFI_HOME}/content_repository \
    && mkdir -p ${NIFI_HOME}/provenance_repository \
    && mkdir -p ${NIFI_HOME}/state \
    && mkdir -p ${NIFI_LOG_DIR} \
    && ln -s ${NIFI_HOME} ${NIFI_BASE_DIR}/nifi-${NIFI_VERSION}

VOLUME ${NIFI_LOG_DIR} \
       ${NIFI_HOME}/conf \
       ${NIFI_HOME}/database_repository \
       ${NIFI_HOME}/flowfile_repository \
       ${NIFI_HOME}/content_repository \
       ${NIFI_HOME}/provenance_repository \
       ${NIFI_HOME}/state

# Clear nifi-env.sh in favour of configuring all environment variables in the Dockerfile
RUN echo "#!/bin/sh\n" > $NIFI_HOME/bin/nifi-env.sh

# Web HTTP(s) & Socket Site-to-Site Ports
EXPOSE 8080 8443 10000

WORKDIR ${NIFI_HOME}
COPY hdfs-site.xml ./
COPY core-site.xml ./
COPY SFTP_TO_HDFS.xml ./SFTP_TO_HDFS.xml
COPY SFTP_TO_HDFS.py ./SFTP_TO_HDFS.py
COPY mysql-connector-java-5.1.38.jar ./mysql/
COPY setenv.sh ./
COPY entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
CMD ["SFTP_TO_HDFS.py"]
