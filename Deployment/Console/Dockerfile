FROM python:3.6.8

# - ARG - Variables that are accessed during Image build
ARG USER=couture
ARG USER_HOME=/home/${USER}
ARG CONSOLE_DIR=${USER_HOME}/Console
#------Copy required files from intermediate container-------
COPY ./Console ${CONSOLE_DIR}

#------install python packages from requirements.txt------
RUN pip install -r  ${CONSOLE_DIR}/requirements.txt

#-----switch user inside container after installation-----
RUN  useradd -ms /bin/bash couture
RUN chown -R couture:couture ${USER_HOME}
USER ${USER}:${USER}

#---------------Application specific changes---------------
WORKDIR ${CONSOLE_DIR}

#------------------Expose required Ports------------------
EXPOSE 5000

#-----------------Run Superset Application-----------------
#docker run --name CONTAINER-NAME-tid -p 8088:8088 -v supersetdb:/home/couture/.superset image:tag
CMD gunicorn -b 0.0.0.0:5000 -w 4 run:app
