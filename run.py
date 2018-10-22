#!/usr/bin/env python

# https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-managedomains-snapshots.html

import argparse
import json
import boto3
import requests
from requests_aws4auth import AWS4Auth

def get_args():
    parser = argparse.ArgumentParser(description='Create snapshot repository in s3 for AWS Elasticsearch')
    parser.add_argument('--region', help='AWS Region, default: us-east-1', required=False, default='us-east-1')
    parser.add_argument('--host', help='AWS Elasticsearch endpoint, i.e. domain-blab-bla-bla.us-east-1.es.amazonaws.com', required=True)
    parser.add_argument('--repo', help='Snapshots repository name, default: s3-snapshots', required=False, default='s3-snapshots')
    parser.add_argument('--bucket', help='S3 bucket for snapshots repo', required=False, default='elasticsearch-snapshots')
    parser.add_argument('--role', help='IAM role arn, default: s3-snapshots', required=False, default='s3-snapshots')

    return vars(parser.parse_args())


if __name__ == "__main__":
  args = get_args()
  region = args['region']

  session = boto3.Session()
  credentials = session.get_credentials()
  awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, 'es', session_token=credentials.token)

  # Register repository
  path = "_snapshot/" + args['repo']  # the Elasticsearch API endpoint
  url = 'https://' + args['host'] + '/' + path

  payload = {
    "type": "s3",
    "settings": {
      "bucket": args['bucket'],
      "region": region,
      "role_arn": args['role']
    }
  }

  headers = {"Content-Type": "application/json"}

  r = requests.put(url, auth=awsauth, data=json.dumps(payload), headers=headers)

  print(r.status_code)
  print(r.text)

