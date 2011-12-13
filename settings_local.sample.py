# Make a copy of this file and name it settings_local.py.

from settings import *

AWS_ACCESS_KEY_ID = '<Your S3 access key>'
AWS_SECRET_ACCESS_KEY = '<Your S3 secret>'

BUCKET_NAME = '<A unique bucket name>'

# Uncomment the lines below to expose additional buckets. This
# one, for instance, will be located at /buckets/testing.
#
#EXTRA_BUCKETS['testing'] = subclass_settings(globals(),
#    BUCKET_NAME='my-testing-bucket',
#    PUBLISH_DOMAIN=None
#    )
