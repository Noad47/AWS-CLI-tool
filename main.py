from Route53 import delete_records


def main():
    while True:
        noa = input("Choose a resource: EC2-instances, S3, Route53: ").strip().lower()
        if noa not in ["ec2-instances", "s3", "route53"]:
            print("Invalid choice. Please select one of the options: EC2-instances, S3, or Route53.")
            continue

        # S3
        if noa == "s3":
            actions = input("Select an action by the number: create (1), upload (2), or list (3): ").strip()
            if actions == "1":
                name_it = input("What's the name of your bucket? ").lower()
                access = input("Do you want your bucket to be private or public? (public/private): ").lower()
                from S3 import creating_s3
                creating_s3(name_it, access)

            elif actions == "2":
                from S3 import listing_s3_buckets
                print(listing_s3_buckets())
                the_bucket = input("Please select the bucket to which the upload should be made from the list above: ").lower()
                the_path = input("Enter the path of the file you want to upload: ").lower()
                filename = input("Enter the name of the file: ").lower()
                from S3 import uploading_files
                uploading_files(the_path, the_bucket, filename)

            elif actions == "3":
                from S3 import listing_s3_buckets
                print(listing_s3_buckets())

            else:
                print("Seems that you had a mistake. Please try again.")
                continue


        # EC2 Instances
        elif noa == "ec2-instances":
            actions = input("Select an action: create, start, stop, or list: ").strip().lower()

            if actions == "create":
                type_of_ec2 = input("Choose instance type - t3.nano or t4g.nano: ").strip().lower()
                name_of_instance = input("Enter instance name: ").strip().lower()
                ami = input("Select OS - Ubuntu or Amazon Linux): ").lower()
                from ec2 import launch_instance
                launch_instance(type_of_ec2, ami, name_of_instance)

            elif actions == "stop":
                from ec2 import stopping_instance
                stopping_instance()

            elif actions == "start":
                from ec2 import starting_instance
                starting_instance()

            elif actions == "list":
                from ec2 import listing
                listing()

            else:
                print("It seems that you had a mistake. The action you want to take is not one of the available options. Please try again.")
                continue

        # Route53
        elif noa == "route53":
            actions = input("What would you like to do?\n Enter '1' to create a hosted zone\n Enter '2' to delete a hosted zone\n Enter '3' to manage records: ").strip()

            if actions == "1":
                zones_name = input("Please enter the full name of the hosted zone (e.g. 'example.com'): ").strip().lower()
                if "."  not in zones_name:
                    print("Invalid input. The hosted zone name must be a valid domain (e.g., example.com). Please try again.")
                    continue
                from Route53 import create_hosted_zones
                create_hosted_zones(zones_name)


            elif actions == "2":
                from Route53 import delete_hosted_zones
                delete_hosted_zones()


            elif actions == "3":
                action = input("Please choose one of the following actions to perform on the record: create, upsert, or delete: ").strip().upper()
                if action not in ["CREATE", 'UPSERT', "DELETE"]:
                    print("please enter one of these: [create, update, delete]")
                    return

                from Route53 import manage_records
                if action == "DELETE":
                    delete_records()
                else:
                    manage_records(action)


            else:
                print("Seems that you made a mistake. Please choose a valid action.")
                continue

        exit_choice = input("Do you want to perform another action? (yes/no): ").lower().strip()
        if exit_choice != "yes":
            print("Exiting the program.")
            break

main()
