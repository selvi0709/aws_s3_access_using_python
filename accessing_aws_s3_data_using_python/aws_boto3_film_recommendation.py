# Accessing aws s3 storage to fetch data for film recommendation

!pip install boto3

import boto3

# Commented out IPython magic to ensure Python compatibility.
# %env AWS_ACCESS_KEY_ID=AKIA4FVO23Z7UTAUDN4V
# %env AWS_SECRET_ACCESS_KEY=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
# %env AWS_DEFAULT_REGION=us-east-1

import boto3
# Retrieve the list of existing buckets
s3 = boto3.client('s3')
response = s3.list_buckets()

# Output the bucket names
print('Existing buckets:')
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')

import boto3
from collections import Counter
import numpy as np
import pandas as pd
from google.colab import files
import logging
import boto3
from botocore.exceptions import ClientError
import os
import json

files.upload()

def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True

create_bucket(bucket_name = "guviseltest")

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

s3 = boto3.client('s3')
with open("small_data.tsv", "rb") as f:
    s3.upload_fileobj(f, "guvisel", "s3_data.tsv")

def download_froms3(bucketname,objectname,filename):
  s3 = boto3.client('s3')
  s3.download_file(bucketname, objectname, filename)

download_froms3('guvisel', 's3_data.tsv', 'download_s3.tsv')

df = pd.read_csv("download_s3.tsv",sep = "\t")


top_movies = Counter(df["movie_id"].values).most_common(10)
movie_suggestions = [x for (x,y) in top_movies]
print(movie_suggestions)

def get_recomendations(user1):
  watched_movies = df[df["user_id"]==user1]["movie_id"]
  return [x for x in movie_suggestions if x not in watched_movies]

predictions = {}
users = df["user_id"].unique()
for user in users:
  try:
   predictions[str(user)] = get_recomendations(user)
  except:
    pass

# pip install numpyencoder

# Refer: https://stackoverflow.com/questions/50916422/python-typeerror-object-of-type-int64-is-not-json-serializable
# Install numpyencoder and import and add in dump method.

# pip install numpyencoder

from numpyencoder import NumpyEncoder

with open('result.json', 'w') as fp:
    json.dump(predictions, fp, cls=NumpyEncoder)

s3 = boto3.client('s3')
with open("result.json", "rb") as f:
    s3.upload_fileobj(f, "guvisel", "movie_list.json")