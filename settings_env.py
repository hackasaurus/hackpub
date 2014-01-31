import os

from settings import *

MAX_PAYLOAD_SIZE = int(os.environ.get('MAX_PAYLOAD_SIZE',
                                      str(MAX_PAYLOAD_SIZE)))

ALLOW_ORIGINS = os.environ.get('ALLOW_ORIGINS', ALLOW_ORIGINS)

PUBLISH_DOMAIN = os.environ.get('PUBLISH_DOMAIN')

ENABLE_PPX = 'ENABLE_PPX' in os.environ

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
BUCKET_NAME = os.environ['BUCKET_NAME']

# Examples:
#
# EXTRABUCKET_TESTING=my-testing-bucket
#   exposes bucket 'my-testing-bucket' at /buckets/testing 
#
# EXTRABUCKET_TESTING=my-testing-bucket@mypublishdomain.com
#   does the same as above but publishes to mypublishdomain.com

def load_extra_buckets():
    for key in os.environ:
        if key.startswith('EXTRABUCKET_'):
            name = os.environ[key]
            slug = key.split('EXTRABUCKET_', 1)[1].lower()
            domain = None
            if '@' in name:
                name, domain = name.split('@')
            EXTRA_BUCKETS[slug] = subclass_settings(globals(),
                BUCKET_NAME=name,
                PUBLISH_DOMAIN=domain
            )

load_extra_buckets()
