from xml.dom.minidom import parseString

import S3
import httplib2
import random

_pub_read_grant = parseString("""<Grant>
  <Grantee xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:type="Group">
    <URI>http://acs.amazonaws.com/groups/global/AllUsers</URI>
  </Grantee>
  <Permission>READ</Permission>
</Grant>""").documentElement

LETTERS = "abcdefghijklmnopqrstuvwxyz"

def generate_random_word(length):
    letters = []
    for i in range(length):
        letters.append(random.choice(LETTERS))
    return ''.join(letters)

class S3Storage(object):
    def __init__(self, access_key_id, secret_access_key, bucket,
                 key_length=8, publish_domain=None, http=None,
                 generate_key=generate_random_word):
        if publish_domain is None:
            publish_domain = '%s.%s' % (bucket, S3.DEFAULT_HOST)
        if http is None:
            http = httplib2.Http()
        self.conn = S3.AWSAuthConnection(access_key_id, secret_access_key)
        self.bucket = bucket
        self.key_length = key_length
        self.publish_domain = publish_domain
        self.http = http
        self.generate_key = generate_key
        if self.conn.check_bucket_exists(bucket).status == 404:
            self.conn.create_located_bucket(bucket, S3.Location.DEFAULT)

    def _published_url(self, key):
        return 'http://%s/%s' % (self.publish_domain, key)

    def _generate_valid_key(self):
        while True:
            key = self.generate_key(self.key_length)
            url = self._published_url(key)
            resp, content = self.http.request(url, method="HEAD")
            if resp.status in [403, 404]:
                return key

    def get_metadata(self, key):
        url = self._published_url(key)
        resp, content = self.http.request(url, method="HEAD")
        if resp.status == 200:
            metakeys = [
                name for name in resp.keys()
            ]
            metadata = {}
            for name in resp.keys():
                if name.startswith(S3.METADATA_PREFIX):
                    prop = name[len(S3.METADATA_PREFIX):]
                    metadata[prop] = resp[name]
            metadata['published-url'] = self._published_url(key)
            return metadata
        return None

    def create(self, content, mimetype, metadata):
        key = self._generate_valid_key()
        obj = S3.S3Object(content, metadata)
        self.conn.put(self.bucket, key, obj, {
            'x-amz-storage-class': 'REDUCED_REDUNDANCY',
            'Content-Type': mimetype,
        })

        aclxml = self.conn.get_acl(self.bucket, key).body
        acl = parseString(aclxml)
        acl.getElementsByTagName('AccessControlList')[0].appendChild(_pub_read_grant)
        self.conn.put_acl(self.bucket, key, acl.toxml())
        return self._published_url(key)
