import boto3
session = boto3.Session()
ec2_client = boto3.client('ec2')
ec2 = session.resource('ec2')



def launch_instance(type_of_ec2, ami, name_of_instance):
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']},{'Name': 'tag:CreatedBy', 'Values': ['CLI']}])
    count = len(list(instances))
    print("You have already "f"{count} instances running.")
    if count == 2:
        print("can't create more than 2 instances")
        return

    if type_of_ec2 not in ["t3.nano","t4g.nano"]:
        print("you must enter one of those types: t3.nano or t4g.nano. try again")
        return
    elif type_of_ec2 == "t3.nano":
        if ami == "ubuntu":
            ami = "ami-04b4f1a9cf54c11d0"
        elif ami == "amazon linux":
            ami = "ami-053a45fff0a704a47"
        else:
            print("you must enter one of those OS: ubuntu or amazon linux. try again")
            return

    elif type_of_ec2 == "t4g.nano":
        if ami == "ubuntu":
            ami = "ami-0a7a4e87939439934"
        elif ami == "amazon linux":
            ami = "ami-0f37c4a1ba152af46"
        else:
            print("you must enter one of those OS: ubuntu or amazon linux. try again")
            return


    instances = ec2.create_instances(
        ImageId=ami,
        MinCount=1,
        MaxCount=1,
        InstanceType=type_of_ec2,
        KeyName='noadavid-keypair',
        SecurityGroupIds=['sg-0381ed0fa0689223c'],
        SubnetId='subnet-0597eea4c68c3bb56',
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': name_of_instance,
                    },
                    {
                        'Key': 'CreatedBy',
                        'Value': 'CLI',
                    },
                    {
                        'Key': 'owner',
                        'Value': 'noadavid'
                    },
                ],

            },
        ],
    )

    instance = instances[0]
    instance.wait_until_running()
    instance.reload()
    print("Instance ID:", instance.id)
    print("Private IP:", instance.private_ip_address)



def stopping_instance():
    test1 = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}, {'Name': 'tag:CreatedBy', 'Values': ['CLI']}])
    running_list = {}
    for instance in test1:
        ids = instance.instance_id
        types = instance.instance_type
        tags = instance.tags
        for i in tags:
            if i["Key"] == "Name":
                names_of_instances = i["Value"]
                running_list[names_of_instances] = ids, types

    if len(running_list) > 0:
        print("The following are all running instances that were created via the CLI:")
        for key, value in running_list.items():
            print(key, ": ", value)

        requested_name = input("from the list above: what is the name of the instance u want to stop: ")
        if requested_name in running_list.keys():
            instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']},
                                                      {'Name': 'tag:Name', 'Values': [requested_name]},
                                                      {'Name': 'tag:CreatedBy', 'Values': ['CLI']}])
            for instance in instances:
                # print(instance.instance_id)
                ec2_client.stop_instances(InstanceIds=[instance.instance_id])
                print("sucess - the instance is stop")
        else:
            print("the requested instances is not in the list.")
    else:
        print("We could not found running instances")
        return



def starting_instance():
    test1 = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}, {'Name':'tag:CreatedBy', 'Values': ['CLI']}])
    stopped_list = {}
    for instance in test1:
        ids = instance.instance_id
        types = instance.instance_type
        tags = instance.tags
        for i in tags:
            if i["Key"] == "Name":
                names_of_instances = i["Value"]
                stopped_list[names_of_instances] = ids, types

    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}, {'Name': 'tag:CreatedBy', 'Values': ['CLI']}])
    count = len(list(instances))
    print("You have already "f"{count} instances running.")
    if count == 2:
        print("can't create more than 2 instances")
        return

    if len(stopped_list) > 0:
        print("These are all the stopped instances that were created through the CLI:")
        for key, value in stopped_list.items():
            print(key, ": ", value)

        requested_name1 = input("from the list above: what is the name of the instance u want to start: ")
        if requested_name1 in stopped_list.keys():
            instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']},
                                                      {'Name': 'tag:Name', 'Values': [requested_name1]},
                                                      {'Name': 'tag:CreatedBy', 'Values': ['CLI']}])
            for instance in instances:
                # print(instance.instance_id)
                ec2_client.start_instances(InstanceIds=[instance.instance_id])
                print("sucess - the instance is start")
        else:
            print("the requested instances is not in the list.")
    else:
        print("We could not found stopped instances. Please try again")
        return





def listing():
    all_instances_cli = {}
    instances = ec2.instances.filter(Filters=[{'Name':'tag:CreatedBy', 'Values': ['CLI']}, {'Name': 'tag:owner', 'Values': ['noadavid']}])
    for instance in instances:
        # print(instance.instance_id)
        ids = instance.instance_id
        types = instance.instance_type
        tags = instance.tags
        # print(tags)
        for i in tags:
            if i["Key"] == "Name":
                # print(i["Value"])
                names_of_instances = i["Value"]
                all_instances_cli[names_of_instances] = ids, types

    for key, value in all_instances_cli.items():
        print(key, ": ", value)
