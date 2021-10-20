import os

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

LINODE_BUCKET = 'cfedemo-ecomm'
LINODE_BUCKET_REGION = 'us-east-1'
LINODE_BUCKET_ACCESS_KEY = os.environ.get("LINODE_BUCKET_ACCESS_KEY")
LINODE_BUCKET_SECRET_KEY = os.environ.get("LINODE_BUCKET_SECRET_KEY")

AWS_S3_ENDPOINT_URL = f'https://{LINODE_BUCKET_REGION}.linodeobjects.com'
AWS_ACCESS_KEY_ID = LINODE_BUCKET_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = LINODE_BUCKET_SECRET_KEY
AWS_S3_REGION_NAME = LINODE_BUCKET_REGION
AWS_S3_USE_SSL = True
AWS_STORAGE_BUCKET_NAME = LINODE_BUCKET