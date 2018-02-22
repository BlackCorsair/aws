#!../cli-ve/bin/python3

import boto3
from botocore.exceptions import ClientError
import pprint
from time import sleep

# Global variables
pp = pprint.PrettyPrinter(indent=2)

# Function which shutdown an instance given the
# instance id


def shutdown_instance(instance_id, ec2):
    try:
        response = ec2.stop_instances(
            InstanceIds=[instance_id],
            DryRun=False
        )
        pp.pprint(response)
    except ClientError as e:
        print(e)


if __name__ == "__main__":
    instance_id = 'some-id'
    ec2 = boto3.client('ec2')
    instance = boto3.resource('ec2').Instance(instance_id)
    code = instance.state.get('Code')
    if 80 == code or 64 == code:
        print("Instance already stopped or stopping.")
        pp.pprint(instance.state)
    else:
        shutdown_instance(instance_id, ec2)
        while(80 != instance.state.get('Code')):
            print("Stopping instance...")
            sleep(5)
            instance = boto3.resource('ec2').Instance(instance_id)
        print("Instance stopped.")
        pp.pprint(instance.state)
