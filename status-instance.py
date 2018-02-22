#!../cli-ve/bin/python3
import boto3
import pprint

devops = boto3.client('ec2')
response = devops.describe_instances(
    InstanceIds=['some-id'],
)
x = response['Reservations'][0]['Instances']
pp = pprint.PrettyPrinter(indent=2)
pp.pprint(x)
print('########################')
print(response.values())
print('########################')

ec2 = boto3.resource('ec2')
instance = ec2.Instance('some-id')
print(instance.network_interfaces_attribute)
