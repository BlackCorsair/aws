#!cli-ve/bin/python3
import boto3
from botocore.exceptions import ClientError
import json
from time import sleep
import pprint

# global variables

pp = pprint.PrettyPrinter(indent=2)
# read conf file and returns json code


def readConf(file):
    f = open(file)
    conf = json.loads(f.read())
    f.close()
    return conf

# checks instance status


def checkStatus(instance_id):
    instance = boto3.resource('ec2').Instance(instance_id)
    while(16 != instance.state.get('Code')):
        print("Starting instances...")
        sleep(5)
        instance = boto3.resource('ec2').Instance(instance_id)
    print("Instance started.")
    pp.pprint(instance.state)

# starts the instance or instances


def startInstances(json_conf, ec2):
    instances = [instance for instance in json_conf['instances']]
    for instance in instances:
        try:
            response = ec2.start_instances(
                InstanceIds=[instance['id']], DryRun=False)
            pp.pprint(response)
        except ClientError as e:
            print(e)
    for instance in instances:
        checkStatus(instance['id'])


if __name__ == "__main__":
    json_conf = readConf("conf.json")
    ec2 = boto3.client('ec2')
    startInstances(json_conf, ec2)
