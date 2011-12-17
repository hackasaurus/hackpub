# Maximum size of a document to be published.
MAX_PAYLOAD_SIZE = 1000000

# Domains that can use our RESTful API. This is delivered as the
# value of the Access-Control-Allow-Origin header. For more information,
# see: https://developer.mozilla.org/en/HTTP_access_control
ALLOW_ORIGINS = '*'

# Domain at which your S3 bucket is exposed. Defaults to
# <BUCKET_NAME>.s3.amazonaws.com. For information on aliasing a domain to
# your bucket, see:
# http://carltonbale.com/how-to-alias-a-domain-name-or-sub-domain-to-amazon-s3
PUBLISH_DOMAIN = None

# Whether to enable PostMessage-Proxy-XMLHttpRequest for browsers
# that don't support CORS. For more information, see:
#
#   https://github.com/toolness/postmessage-proxied-xhr/#readme
#
# WARNING: At the time of this writing, the PPX server iframe will
# grant postMessage-proxied access to the whole server, not just
# individual paths, which may be a security vulnerability if
# multiple hackpub instances are multiplexed off the same domain,
# or if the hackpub instance is part of a bigger web server.
ENABLE_PPX = False

EXTRA_BUCKETS = {}

def subclass_settings(globs, **kwargs):
    class SettingsSubclass(object):
        pass
    
    subclass = SettingsSubclass()
    subclass.__dict__.update(globs)
    subclass.__dict__.update(kwargs)

    return subclass
