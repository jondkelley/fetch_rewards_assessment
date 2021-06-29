#!/usr/bin/env python3
# boto3==1.17.98

import boto3
import yaml
import json
import uuid
from os import environ

this_uuid = str(uuid.uuid4())
aws_region = environ.get('aws_region', 'us-east-2')
ec2 = boto3.resource('ec2', region_name=aws_region)
tag_name = 'jonathankelley'

with open('config.yaml', 'r') as f:
    try:
        conf = yaml.safe_load(f)['server']
        #print(json.dumps(conf, indent=3))
    except yaml.YAMLError as exc:
        print(exc)


def get_ebs_mapping():
    """
    isolate the ebs volume mappings from supplied config file
    """
    volumes = []
    for disk in conf['volumes']:
        volume = {}
        for k, v in disk.items():
            if k == 'device':
                k = 'DeviceName'
                volume[k] = v
            elif k == 'size_gb':
                volume['Ebs'] = {
                    'DeleteOnTermination': True,
                    'VolumeSize': v,
                    'VolumeType': 'gp2'
                }
        volumes.append(volume)
    return volumes


def get_blockvolume_userdata():
    """
    builds the userdata portion for extra block volumes
    """
    script = ""
    for disk in conf['volumes']:
        if disk['mount'] != '/':
            script = script + f"""
# extra volume {disk['mount']}
sudo mkfs.{disk['type']} {disk['device']}
sudo mkdir {disk['mount']}
sudo mount -o defaults {disk['device']} {disk['mount']}
sudo chgrp dataoperator /data
chmod 775 /data"""
    return script


def get_ssh_userdata():
    """
    builds the userdata portion for the ssh public key authentication
    """
    script = ""
    for user in conf['users']:
        script = script + f"""
# setup ssh {user['login']}
sudo adduser {user['login']}
usermod -a -G dataoperator {user['login']}
sudo mkdir /home/{user['login']}/.ssh
sudo chmod 700 /home/{user['login']}/.ssh
sudo echo "{user['ssh_key']}" > /home/{user['login']}/.ssh/authorized_keys
sudo chmod 600 /home/{user['login']}/.ssh/authorized_keys
sudo chown {user['login']}:{user['login']} /home/{user['login']}/.ssh
sudo chown {user['login']}:{user['login']} /home/{user['login']}/.ssh/authorized_keys
        """
    return script


def get_userdata():
    user_data = """#!/bin/bash
groupadd dataoperator
    """ + get_blockvolume_userdata() + get_ssh_userdata()
    return user_data


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
ssmclient = boto3.Session()
ssm = ssmclient.client('ssm')

ssm_query = '/aws/service/ami-amazon-linux-latest/{}-ami-{}-{}-gp2'.format(
    conf['ami_type'],
    conf['virtualization_type'],
    conf['architecture'])

select_ami = ssm.get_parameter(Name=ssm_query)['Parameter']['Value']


def create_vpc():
    """
    create the vpc for this exercise
    """
    vpc = ec2.create_vpc(CidrBlock='192.168.0.0/16')
    vpc.create_tags(Tags=[{"Key": "Name", "Value": tag_name}])
    vpc.wait_until_available()
    print(f'Created vpc {vpc.id}')
    return vpc


def create_igw(vpc):
    """
    create and attach internet gateway
    """
    ig = ec2.create_internet_gateway()
    vpc.attach_internet_gateway(InternetGatewayId=ig.id)
    print(f'Created interget gateway {ig.id}')
    return ig


def create_rtb(ig, vpc):
    """
    create a routing table with a public routing
    """
    route_table = vpc.create_route_table()
    route = route_table.create_route(
        DestinationCidrBlock='0.0.0.0/0',
        GatewayId=ig.id
    )
    print(f'Created route table {route_table.id}')

    # create a subnet
    subnet = ec2.create_subnet(CidrBlock='192.168.1.0/24', VpcId=vpc.id, TagSpecifications=[
                               {'ResourceType': 'subnet', 'Tags': [{'Key': 'Name', 'Value': tag_name}]}])
    print(f'Created subnet {subnet.id}')

    # associate a route table with this subnet
    route_table.associate_with_subnet(SubnetId=subnet.id)
    return subnet


def create_sg(vpc):
    """
    create security group
    """
    # create security group
    sec_group = ec2.create_security_group(
        GroupName='slice_0', Description='slice_0 sec group', VpcId=vpc.id)
    # ping
    sec_group.authorize_ingress(
        CidrIp='0.0.0.0/0',
        IpProtocol='icmp',
        FromPort=-1,
        ToPort=-1
    )
    # ssh
    sec_group.authorize_ingress(
        CidrIp='0.0.0.0/0',
        IpProtocol='tcp',
        FromPort=22,
        ToPort=22
    )
    print(f'Created security group {sec_group.id}')
    return sec_group


def create_vm(sec_group, subnet):
    """
    create an ec2 instance vm
    """
    instances = ec2.create_instances(
        BlockDeviceMappings=get_ebs_mapping(),
        ImageId=select_ami,
        InstanceType=conf['instance_type'],
        MaxCount=conf['max_count'],
        MinCount=conf['min_count'],
        UserData=get_userdata(),
        NetworkInterfaces=[{'SubnetId': subnet.id,
                            'DeviceIndex': 0,
                            'AssociatePublicIpAddress': True,
                            'Groups': [sec_group.group_id]}],
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': tag_name
                    },
                    {
                        'Key': 'Candidate',
                        'Value': 'Jonathan Kelley'
                    },
                    {
                        'Key': 'Uuid',
                        'Value': this_uuid
                    },
                ]
            },
        ])

    print('⏳ Spinning up Xen VM... wait a few moment(s).')
    instances[0].wait_until_running()
    print(f'Created instance {instances[0].id}')


def get_vm_details():
    """
    describe the instance and print the ssh login commands for the layman
    """
    session = boto3.session.Session(region_name=aws_region)
    client = session.client('ec2')
    reservations = client.describe_instances(
        Filters=[{'Name': 'tag:Uuid', 'Values': [this_uuid]}])
    for reservation in reservations["Reservations"]:
        for instance in reservation["Instances"]:
            print('You can SSH to your shiny new VM with one of the following commands:')
            ipaddr = instance.get('PublicIpAddress')
            for user in conf['users']:
                login = user['login']
                print(f'\tssh {login}@{ipaddr}')


if __name__ == "__main__":
    # kick off the script parts
    vpc = create_vpc()
    ig = create_igw(vpc)
    subnet = create_rtb(ig, vpc)
    sec_group = create_sg(vpc)
    create_vm(sec_group, subnet)
    get_vm_details()
