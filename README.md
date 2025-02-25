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
