
from kubernetes import client, config
#config.load_incluster_config()

ENV_LIST = {
    'LANG': "C.UTF-8",
    'JOB_ID': "0",
    'SFTP_HOSTNAME': "ec2-3-17-129-179.us-east-2.compute.amazonaws.com",
    'SFTP_USERNAME': "nifi-test",
    'SFTP_PASSWORD': "nifi-test",
    'SFTP_REMOTE_PATH': "/home/nifi-test/random_data",
    'HADOOP_DIRECTORY': "/nifi-kube",
    'SQL_HOST': "172.31.29.168",
    'SQL_PORT': "30868",
    'SQL_USER': "root",
    'SQL_PASS': "password",
    'SQL_DB': "CoutureConsoleDB"
}
ENV_LIST['HADOOP_CONFIGURATION_RESOURCES']="/opt/nifi/nifi-current/hdfs-site.xml,/opt/nifi/nifi-current/core-site.xml"


def getJobBody(namespace='couture-console', jobname='nifi-test', containername='nifi-test', containerimage='sidharthc/nifi-test:alpha', env_vars=ENV_LIST, containerargs=['SFTP_TO_HDFS.py']):
    body = client.V1Job(api_version="batch/v1", kind="Job")
    # Body needs Metadata
    # Attention: Each JOB must have a different name!
    body.metadata = client.V1ObjectMeta(namespace=namespace, name=jobname)
    # And a Status
    body.status = client.V1JobStatus()
    # Now we start with the Template...
    template = client.V1PodTemplate()
    template.template = client.V1PodTemplateSpec()
    env_list = []
    for env_name, env_value in env_vars.items():
        env_list.append( client.V1EnvVar(name=env_name, value=env_value) )
    container = client.V1Container(name=containername, image=containerimage, args=containerargs, env=env_list)
    template.template.spec = client.V1PodSpec(containers=[container], restart_policy='Never')
    # And finaly we can create our V1JobSpec!
    body.spec = client.V1JobSpec(ttl_seconds_after_finished=100, template=template.template)
    return body

api_instance = client.BatchV1Api(client.ApiClient(client.Configuration()))
