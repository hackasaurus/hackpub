# Maximum size of a document to be published.
MAX_PAYLOAD_SIZE = 100000

# Domains that can use our RESTful API. This is delivered as the
# value of the Access-Control-Allow-Origin header. For more information,
# see: https://developer.mozilla.org/en/HTTP_access_control
ALLOW_ORIGINS = '*'

# Domain at which your S3 bucket is exposed. Defaults to
# <BUCKET_NAME>.s3.amazonaws.com. For information on aliasing a domain to
# your bucket, see:
# http://carltonbale.com/how-to-alias-a-domain-name-or-sub-domain-to-amazon-s3
PUBLISH_DOMAIN = None
