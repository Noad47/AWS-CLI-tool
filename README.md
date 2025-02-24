# AWS CLI Tool

## Introduction
This Python-based CLI tool allows developers to manage AWS resources, including EC2 instances, S3 buckets, and Route 53 DNS zones. It provides a structured and secure way to interact with AWS services.

## Features

### EC2 Instances
- **Create**: Supports creating instances of type `t3.nano` or `t4g.nano`, with a limit of two running instances.
- **AMI Selection**: Choose between the latest Ubuntu AMI or Amazon Linux AMI.
- **Manage Instances**: Start and stop instances, but only if they were created through this CLI.
- **List Instances**: Display a list of all EC2 instances created by this tool.

### S3 Buckets
- **Create**: Supports creating S3 buckets with public or private access.
- **Public Bucket Confirmation**: Requests additional approval when selecting public access.
- **Upload Files**: Allows uploading files only to buckets created by this CLI.
- **List Buckets**: Shows a list of S3 buckets created via the CLI.

### Route 53
- **Create Zones**: Enables the creation of DNS zones via Route 53.
- **Manage DNS Records**: Allows creating, updating, and deleting DNS records, but only for zones created via this CLI.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure AWS credentials are configured using `aws configure`.

## Usage
Run the CLI tool using:
```bash
python main.py <resource> <action> [parameters]
```

### Example Commands
- Create an EC2 instance:
  ```bash
  python main.py ec2 create --instance-type t3.nano --ami ubuntu
  ```
- List all EC2 instances created via the CLI:
  ```bash
  python main.py ec2 list
  ```
- Create an S3 bucket:
  ```bash
  python main.py s3 create --name my-bucket --access private
  ```
- Upload a file to an S3 bucket:
  ```bash
  python main.py s3 upload --bucket my-bucket --file myfile.txt
  ```
- Create a Route 53 zone:
  ```bash
  python main.py route53 create --domain example.com
  ```

## Security Best Practices
- Ensure AWS credentials are **not** hardcoded in the project.
- Use IAM roles and policies with the least privileges required.
- Enable logging and monitoring for security audits.

## Project Structure
- `main.py`: Entry point of the CLI, calling functions from resource modules.
- `ec2.py`: Contains EC2-related functions.
- `s3.py`: Handles S3 operations.
- `route53.py`: Manages Route 53 DNS operations.

## License
This project is licensed under the MIT License.

## Contributors
- [Your Name] - Initial development

## Future Improvements
- Implement better error handling.
- Add support for additional AWS resources.

