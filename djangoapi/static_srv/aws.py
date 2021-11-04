import datetime
import os

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")


#python manage.py collectstatic

print('aws credentials from conf...',AWS_ACCESS_KEY_ID,'  secret :',AWS_SECRET_ACCESS_KEY)

AWS_GROUP_NAME = "cpatech_dev"
AWS_USERNAME = "cpatech_awsadmin"

AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = False

DEFAULT_FILE_STORAGE = 'djangoapi.static_srv.utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'djangoapi.static_srv.utils.StaticRootS3BotoStorage'
#AWS_STORAGE_BUCKET_NAME = 'techcpa-aws-1'
AWS_STORAGE_BUCKET_NAME = 'cpatech-dev-1'
S3DIRECT_REGION = 'us-east-2'
S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = MEDIA_URL
STATIC_URL = S3_URL + 'static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

two_months = datetime.timedelta(days=61)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_HEADERS = {
    'Expires': expires,
    'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()), ),
}

PROTECTED_DIR_NAME = 'protected'
PROTECTED_MEDIA_URL = '//%s.s3.amazonaws.com/%s/' % (
    AWS_STORAGE_BUCKET_NAME, PROTECTED_DIR_NAME)

# Link time until expire
AWS_DOWNLOAD_EXPIRE = 5000  # (0ptional, in milliseconds)
print('aws login from  group name...',AWS_GROUP_NAME,'  username :',AWS_USERNAME,' aws bucket ',AWS_STORAGE_BUCKET_NAME)