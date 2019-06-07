export SFTP_HOSTNAME='ec2-3-17-129-179.us-east-2.compute.amazonaws.com'
export SFTP_USERNAME='nifi-test'
export SFTP_PASSWORD='nifi-test'
export SFTP_REMOTE_PATH='/home/nifi-test/random_data'
export HADOOP_CONFIGURATION_RESOURCES='/opt/nifi/nifi-current/hdfs-site.xml,/opt/nifi/nifi-current/core-site.xml'
export HADOOP_DIRECTORY='/nifi-test'
export PUTSQLGET_SQL_STATEMENT="insert into NifiTest.Jobs values('\${filename}', 0);"
export PUTSQLPUT_SQL_STATEMENT="insert into NifiTest.Jobs values('\${filename}', 1) on duplicate key update TRANSFERRED = 1;"
