# AWS CLI Tool

## Introduction
This Python-based CLI tool allows developers to manage AWS resources, including EC2 instances, S3 buckets, and Route 53 DNS zones. It provides a structured and secure way to interact with AWS services via a command-line interface.

## Features

### EC2 Instances
- **Create**: Supports creating instances of type `t3.nano` or `t4g.nano`, with a limit of two running instances at any time.
- **AMI Selection**: Choose between the latest Ubuntu AMI or Amazon Linux AMI.
- **Manage Instances**: Start and stop instances, but only if they were created through this CLI.
- **List Instances**: Display a list of all EC2 instances created by this tool.

### S3 Buckets
- **Create**: Supports creating S3 buckets with public or private access.
- **Public Bucket Confirmation**: Requests additional approval when selecting public access.
- **Upload Files**: Allows uploading files only to buckets created by this CLI. The tool first lists all available buckets before allowing file uploads.
- **List Buckets**: Shows a list of S3 buckets created via the CLI.

### Route 53
- **Create Zones**: Enables the creation of DNS zones via Route 53.
- **Manage DNS Records**: Allows creating, updating, and deleting DNS records, but only for zones created via this CLI.
- **Persistent Tracking**: The CLI maintains a JSON file that records all hosted zones created or deleted through this tool. When listing hosted zones, the CLI only displays those managed by the CLI, ensuring consistency and control.

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
python main.py
```

### Interactive Command Flow
The CLI prompts the user to choose a resource (`EC2-instances`, `S3`, or `Route53`) and then select an action.

#### Example User Flow
- **EC2 Instance Creation**:
  1. Select `EC2-instances`.
  2. Choose `create`.
  3. Select an instance type (`t3.nano` or `t4g.nano`).
  4. Enter an instance name.
  5. Select an OS (`Ubuntu` or `Amazon Linux`).
  6. The instance is created.

- **S3 File Upload**:
  1. Select `S3`.
  2. Choose `upload`.
  3. The CLI lists all available buckets created by the tool.
  4. Select a bucket and provide a file path.
  5. The file is uploaded.

- **Route53 Record Management**:
  1. Select `Route53`.
  2. Choose `create`, `delete`, or `manage records`.
  3. Follow prompts to specify the domain and records.
  4. The hosted zone list updates dynamically based on the user's actions.

## Security Best Practices
- Ensure AWS credentials are **not** hardcoded in the project.
- Use IAM roles and policies with the least privileges required.
- Enable logging and monitoring for security audits.

## Project Structure
- `main.py`: Entry point of the CLI, prompting users and calling functions from resource modules.
- `ec2.py`: Contains EC2-related functions (launching, starting, stopping, listing instances).
- `s3.py`: Handles S3 operations (creating buckets, listing, uploading files).
- `route53.py`: Manages Route 53 DNS operations and maintains a JSON file to track created/deleted hosted zones.

## License
This project is licensed under the MIT License.

## Contributors
- Noad David - Initial development

## Future Improvements
- Implement better error handling.
- Add support for additional AWS resources.

