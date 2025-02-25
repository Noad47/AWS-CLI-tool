import ipaddress
from time import process_time
import json
import boto3
import datetime
import botocore
from botocore.exceptions import ClientError

route53 = boto3.client('route53')
paginator = route53.get_paginator('list_resource_record_sets')


x = str(datetime.datetime.now())


FILE_PATH = r"C:\Users\Owner\PycharmProjects\PythonProject5\hosted_zones.json"
with open(FILE_PATH, "r") as f:
    list_of_hosted_zones = json.load(f)



def create_hosted_zones(zones_name):
    if zones_name not in list_of_hosted_zones:
        try:
            creation = route53.create_hosted_zone(Name= zones_name, CallerReference= x)
            # print(creation)
            b = creation['HostedZone']['Id']
            ID = b[12:]
            list_of_hosted_zones[zones_name] = ID
            # print(list_of_hosted_zones)
            with open(FILE_PATH, "w") as f:
                json.dump(list_of_hosted_zones, f, indent=4)

            route53.change_tags_for_resource(
                ResourceType='hostedzone',
                ResourceId=ID,
                AddTags=[{'Key': 'owner','Value': 'noad'},{'Key': 'createdby', 'Value': 'CLI'}])
            print("success - the hosted zone was created")

        except:
            print(f"{zones_name} is might be reserved by AWS")
            return
    else:
        print("Here is the list of hosted zones that were created by CLI:", list_of_hosted_zones)
        print("As u can see, this name already exists in our list. please try again with a new name.")
        return





def delete_hosted_zones():
    print("There are all the hosted zones that were created by CLI: ",list_of_hosted_zones)
    delete_request = input("Which of the above would you like to delete (enter the Name): ").strip().lower()
    if delete_request in list_of_hosted_zones:
        try:
            route53.delete_hosted_zone(
                Id=list_of_hosted_zones[delete_request]
            )
            del list_of_hosted_zones[delete_request]
            print("Hosted Zone deleted successfully.")
            print(f"Here is the updated list of hosted zones created using the CLI tool: {list_of_hosted_zones}")
            with open(FILE_PATH, "w") as f:
                json.dump(list_of_hosted_zones, f, indent=4)
        except ClientError as e:
            if 'HostedZoneNotEmpty' in str(e):
                print(f"Error: The hosted zone '{delete_request}' contains non-required resource record sets and so cannot be deleted. You can delete these records first, and then try deleting the hosted zone again.")

            else:
                print(f"An error occurred: {e}")
    else:
        print("We can't find the requested hosted zone. Please check if the ID is correct")





def list_records_with_ip(hosted_zone_id):
    type_of_record = 'A'
    paginator = route53.get_paginator('list_resource_record_sets')

    all_records = []

    for page in paginator.paginate(HostedZoneId=hosted_zone_id):
        # print(page)
        for record in page['ResourceRecordSets']:
            if 'ResourceRecords' in record and record['Type'] == type_of_record:
                for resource in record['ResourceRecords']:
                    if 'Value' in resource:
                        all_records.append({
                            'Record Name': record['Name'],
                            'IP': resource['Value']
                        })

    return all_records




def manage_records(action):
    if action not in ["CREATE", 'UPSERT']:
        print("please enter one of these: [create, update, delete]")
        return

    print("Here are all the hosted zones created by the CLI, along with their IDs: ")
    print(list_of_hosted_zones)
    hosted_zone_name = input("On which hosted zone do you want to take action (choose only from the list above): ").lower().strip()
    if hosted_zone_name not in list_of_hosted_zones:
        print("we can't find the requested name. Please enter the name or ID of the hosted zone. Here is the list: ",list_of_hosted_zones)
        return
    hosted_zone_id = list_of_hosted_zones[hosted_zone_name]


    if action == "UPSERT":
        print(list_records_with_ip(hosted_zone_id))

    record_name = input("Please enter only the record name (e.g. 'RECORD1'). The domain (hosted zone) will be automatically added to the record: ").lower().strip()
    the_real_record_name = record_name + '.' + hosted_zone_name
    print(the_real_record_name)

    ip = input("Enter the desired IP address: ").strip()
    try:
        ipaddress.ip_address(ip)
        print("Valid IP address")
    except ValueError:
        print("Invalid IP address. Please try again.")
        return


    zone_id = list_of_hosted_zones[hosted_zone_name]
    route53.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            'Changes': [
                {
                    'Action': action,
                    'ResourceRecordSet': {
                        'Name': the_real_record_name,
                        'ResourceRecords': [
                            {
                                'Value': ip,
                            },
                        ],
                        'TTL': 60,
                        'Type': 'A',
                    },
                },
            ]
        },
    )
    print("Record deleted successfully.")


def delete_records():
    print("Here are all the hosted zones created by the CLI, along with their IDs: ")
    print(list_of_hosted_zones)
    hosted_zone_name = input("On which hosted zone do you want to take action (choose only from the list above): ").lower().strip()
    if hosted_zone_name not in list_of_hosted_zones:
        print("we cant find the requested name. please enter the name or ID of the hosted zone. Here is the list: ", list_of_hosted_zones)
        return
    hosted_zone_id = list_of_hosted_zones[hosted_zone_name]

    # זה בעצם אומר שזה מדפיס לך את הרשימה של הרקורדים בנמצאים בהוסטזון שבחרת
    print(list_records_with_ip(hosted_zone_id))
    if len(list_records_with_ip(hosted_zone_id)) == 0:
        print("As you can see above, the specified hosted zone doesn't contains non-required resource record. It doesn't have available records")
        return
    record_name = input("Please enter the full Name of the record you want to delete including the hosted zone name (choose only from the list above): ").lower().replace(" ", "").strip()
    the_real_record_name = record_name
    # print(the_real_record_name)
    ip = input("Enter the IP address of the record you chose: ").strip()
    try:
        ipaddress.ip_address(ip)
        print("Valid IP address")
    except ValueError:
        print("Invalid IP address. Please try again.")
        return

    try:
        if hosted_zone_name in list_of_hosted_zones:
            zone_id = list_of_hosted_zones[hosted_zone_name]
            route53.change_resource_record_sets(
                HostedZoneId=zone_id,
                ChangeBatch={
                    'Changes': [
                        {
                            'Action': 'DELETE',
                            'ResourceRecordSet': {
                                'Name': the_real_record_name,
                                'ResourceRecords': [
                                    {
                                        'Value': ip,
                                    },
                                ],
                                'TTL': 60,
                                'Type': 'A',
                            },
                        },
                    ]
                },
            )
            print("Record deleted successfully.")

    except botocore.exceptions.BotoCoreError as e:
            print(f"Error: {e}")
            print("The record you are trying to delete was not found in the hosted zone.")
    except botocore.exceptions.EndpointConnectionError as e:
        print("There was an issue with the endpoint connection:", e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
