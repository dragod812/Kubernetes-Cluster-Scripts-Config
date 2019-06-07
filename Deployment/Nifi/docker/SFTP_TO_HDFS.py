# Nifi Script that will be used to fill metadata for SFTP_TO_HDFS data ingestion
import nipyapi
import os
from nipyapi.nifi.models.processor_config_dto import ProcessorConfigDTO
from nipyapi.nifi.models.controller_service_dto import ControllerServiceDTO
import time

def get_processor(name, processor_list) :
	for p in processor_list :
		if(p.component.name == name) :
			return p
	return None

# get docker ip
import socket
host_ip = socket.gethostbyname(socket.gethostname())

# set the nifi configs
nipyapi.config.nifi_config.host = 'http://'+host_ip+':8080/nifi-api'
nipyapi.config.registry_config.host = 'http://'+host_ip+':8080/nifi-registry-api'

import time
import socket

#get environment variables
sql_host = os.environ['SQL_HOST']
sql_port = os.environ['SQL_PORT']
sql_user = os.environ['SQL_USER']
sql_password = os.environ['SQL_PASS']
sql_db = os.environ['SQL_DB']
job_id = os.environ['JOB_ID']
#wait for nifi to start
def wait_for_port(port=8080, host='localhost', timeout=5.0):
    """Wait until a port starts accepting TCP connections.
    Args:
        port (int): Port number.
        host (str): Host address on which the port should exist.
        timeout (float): In seconds. How long to wait before raising errors.
    Raises:
        TimeoutError: The port isn't accepting connection after time specified in `timeout`.
    """
    start_time = time.perf_counter()
    while True:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                break
        except OSError as ex:
            time.sleep(0.01)
            if time.perf_counter() - start_time >= timeout:
                raise TimeoutError('Waited too long for the port {} on host {} to start accepting '
                                   'connections.'.format(port, host)) from ex
print('waiting for nifi...')
wait_for_port(port=8080, host=host_ip, timeout=60)
print('nifi available...')

#upload required templates
pg_id = nipyapi.canvas.get_root_pg_id()
SFTP_TO_HDFS_template = nipyapi.templates.upload_template(pg_id, 'SFTP_TO_HDFS.xml')

#deploy templates
nipyapi.templates.deploy_template(pg_id, SFTP_TO_HDFS_template.id)
print('template deployed')


# get process group and list all the processor
SFTP_TO_HDFS = nipyapi.canvas.get_process_group('SFTP_TO_HDFS')
SFTP_TO_HDFS_processors = nipyapi.canvas.list_all_processors(SFTP_TO_HDFS.id)

#get DBConnection Pool
print('updating connection pool')
DBcontroller = nipyapi.canvas.get_controller('DBCPConnectionPool', identifier_type='name', bool_response=False)
#update DBConnection Pool
properties = DBcontroller.to_dict()['component']['properties']
properties['Database Connection URL'] = 'jdbc:mysql://' + sql_host + ':' + sql_port + '/' + sql_db
properties['Database User'] = sql_user
properties['Password'] = sql_password
newConfig = ControllerServiceDTO(properties = properties)
nipyapi.canvas.update_controller(DBcontroller, newConfig)
DBcontroller = nipyapi.canvas.get_controller('DBCPConnectionPool', identifier_type='name', bool_response=False)
#schedule the DBCPConnectionPool
nipyapi.canvas.schedule_controller(DBcontroller, True, refresh=False)

# get required processors
ListSFTP= get_processor('ListSFTP', SFTP_TO_HDFS_processors)
PutSQLGET = get_processor('PutSQLGET', SFTP_TO_HDFS_processors)
GetSFTP = get_processor('GetSFTP', SFTP_TO_HDFS_processors)
PutHDFS = get_processor('PutHDFS', SFTP_TO_HDFS_processors)
ListHDFS = get_processor('ListHDFS', SFTP_TO_HDFS_processors)
PutSQLPUT = get_processor('PutSQLPUT', SFTP_TO_HDFS_processors)

#update ListSFTP processor
ListSFTP_dict= ListSFTP.to_dict()
properties = ListSFTP_dict[ 'component' ][ 'config' ][ 'properties' ]
properties['Hostname'] = os.environ['SFTP_HOSTNAME'] #'ec2-18-218-72-133.us-east-2.compute.amazonaws.com'
properties['Username'] = os.environ['SFTP_USERNAME'] #'ubuntu'
properties['Password'] = os.environ['SFTP_PASSWORD'] #'ubuntu'
properties['Remote Path'] = os.environ['SFTP_REMOTE_PATH'] #'/home/ubuntu/kubernetes'
properties['Search Recursively'] = 'true'
newConfig = ProcessorConfigDTO(properties=properties)
nipyapi.canvas.update_processor(ListSFTP, newConfig)


# update 'PutSQLGET' processor
PutSQLGET_dict= PutSQLGET.to_dict()
properties = PutSQLGET_dict[ 'component' ][ 'config' ][ 'properties' ]
properties['putsql-sql-statement'] = "insert into CoutureConsoleDB.DataLoadFile values(" + job_id + ", '${filename}', 0);"
newConfig = ProcessorConfigDTO(properties=properties)
nipyapi.canvas.update_processor(PutSQLGET, newConfig)

# update getsftp processor
GetSFTP_dict = GetSFTP.to_dict()
properties = GetSFTP_dict[ 'component' ][ 'config' ][ 'properties' ]
properties['Hostname'] = os.environ['SFTP_HOSTNAME'] #'ec2-18-218-72-133.us-east-2.compute.amazonaws.com'
properties['Username'] = os.environ['SFTP_USERNAME'] #'ubuntu'
properties['Password'] = os.environ['SFTP_PASSWORD'] #'ubuntu'
properties['Remote Path'] = os.environ['SFTP_REMOTE_PATH'] #'/home/ubuntu/kubernetes'
properties['Search Recursively'] = 'true'
newConfig = ProcessorConfigDTO(properties=properties)
nipyapi.canvas.update_processor(GetSFTP, newConfig)

# update 'PutHDFS' processor
PutHDFS_dict = PutHDFS.to_dict()
properties = PutHDFS_dict[ 'component' ][ 'config' ][ 'properties' ]
# properties['Hadoop Configuration Resources'] = os.environ['HADOOP_CONFIGURATION_RESOURCES'] #'/home/nifi/hadoop/hdfs-site.xml,/home/nifi/hadoop/core-site.xml'
properties['Directory'] = os.environ['HADOOP_DIRECTORY'] #'/temp1'
newConfig = ProcessorConfigDTO(properties=properties)
nipyapi.canvas.update_processor(PutHDFS, newConfig)

#update ListHDFS processor
ListHDFS_dict = ListHDFS.to_dict()
properties = ListHDFS_dict[ 'component' ][ 'config' ][ 'properties' ]
# properties['Hadoop Configuration Resources'] = os.environ['HADOOP_CONFIGURATION_RESOURCES'] #'/home/nifi/hadoop/hdfs-site.xml,/home/nifi/hadoop/core-site.xml'
properties['Directory'] = os.environ['HADOOP_DIRECTORY'] #'/temp1'
newConfig = ProcessorConfigDTO(properties=properties)
nipyapi.canvas.update_processor(ListHDFS, newConfig)

# update 'PutSQLPUT' processor
PutSQLPUT_dict = PutSQLPUT.to_dict()
properties = PutSQLPUT_dict[ 'component' ][ 'config' ][ 'properties' ]
properties['putsql-sql-statement'] = "insert into CoutureConsoleDB.DataLoadFile values(" + job_id + ", '${filename}', 1) on duplicate key update transferred = 1;"
newConfig = ProcessorConfigDTO(properties=properties)
nipyapi.canvas.update_processor(PutSQLPUT, newConfig)

print('updated nifi-processors...');
time.sleep(30)

#schedule the process group
print('Scheduling process_group...')
nipyapi.canvas.schedule_process_group(SFTP_TO_HDFS.id, True)

import MySQLdb

# Connect
db = MySQLdb.connect(host=sql_host, port=int(sql_port),user=sql_user, passwd=sql_password, db=sql_db)


# Execute SQL select statement
time.sleep(20)
query_for_job = "SELECT transferred FROM CoutureConsoleDB.DataLoadFile where job_id = " + job_id + ";"
flag = False
print('waiting for file transfer...')
while(True) :
    cursor = db.cursor()
    cursor.execute(query_for_job)
    results = cursor.fetchall()
    if len(results) == 0 :
        break
    flag = True
    for row in results :
        if row[0] == 0 :
            flag = False
            break
    if flag :
        break
    time.sleep(5)

if not flag :
    print('error on sql side')
    time.sleep(300)
else :
    print('File Transfer Completed')
db.close()
