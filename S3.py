from os import access
from tkinter.font import names

import uuid
import boto3
from pyasn1.type.tag import TagSet

s3 = boto3.client('s3', region_name='us-east-1')


def creating_s3(name_it,access):
    try:
        unique_suffix = uuid.uuid4().hex[:6]  # לוקחים 6 תווים ראשונים מזהה ייחודי
        bucket_name = f"{name_it}-{unique_suffix}"
        print(f"this is the full name of your bucket: '{bucket_name}'")

        if access == "private":
            s3.create_bucket(Bucket=bucket_name)
            print(f"The bucket '{bucket_name}' was created successfully!")
        elif access == "public":
            approval = input("are u sure u want to create public bucket (yes/no): ").lower().strip()
            if approval == "yes":
                s3.create_bucket(Bucket=bucket_name)
                s3.delete_public_access_block(Bucket=bucket_name)
                print(f"The bucket '{bucket_name}' was created successfully!")
            elif approval == "no":
                return
    except:
        print(f"Something went wrong")
    else:
        s3.put_bucket_tagging(
            Bucket=bucket_name,
            Tagging={
                'TagSet': [
                    {
                        'Key': 'createdby',
                        'Value': 'cli'
                    },
                    {
                       'Key': 'owner',
                        'Value': 'noadavid'
                    },
                ]
            },
        )


def listing_s3_buckets():
    names = []
    list_of_buckets = set()
    listing = s3.list_buckets()
    for i in listing["Buckets"]:
        names.append(i["Name"])
    # print(names)
    for name in names:
        try:
            tags = s3.get_bucket_tagging(Bucket=name)
            # print(tags)
            for d in tags['TagSet']:
                if d["Value"] == "noadavid" and d["Key"] == "owner":
                    list_of_buckets.add(name)
                elif d["Value"] == "cli" and d["Key"] == "createdby":
                    list_of_buckets.add(name)
        except:
            pass

    print("This is the list of buckets that were created by CLI:")
    for bucket in list_of_buckets:
        print(f"- {bucket}")
    return list_of_buckets



def uploading_files(filename, the_bucket, the_real):
    existing_buckets = listing_s3_buckets()
    if the_bucket in existing_buckets:
        s3.upload_file(filename, the_bucket, the_real)
        print(f"File '{filename}' uploaded successfully to bucket '{the_bucket}'.")
    else:
        print("there is no bucket with this name in the list")
