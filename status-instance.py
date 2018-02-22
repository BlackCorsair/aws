#!../cli-ve/bin/python3
import boto3
import json
import pprint

devops = boto3.client('ec2')
response = devops.describe_instances(
    InstanceIds=['i-0fe762bcfa85f7716'],
)
x = response['Reservations'][0]['Instances']
pp = pprint.PrettyPrinter(indent=2)
pp.pprint(x)
print('########################')
print(response.values())
print('########################')

ec2 = boto3.resource('ec2')
instance = ec2.Instance('i-0fe762bcfa85f7716')
print(instance.network_interfaces_attribute)
