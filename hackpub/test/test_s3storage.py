from hackpub.s3storage import S3Storage, generate_random_word
import S3

def log(msg):
    print msg

def make_repeated_keygen():
    """
    key generator that conveniently returns the same key for its
    first and second calls, to force execution of the
    collision resolution algorithm.
    """

    keys = []
    for i in range(2):
        keys.append(generate_random_word(8))
    keys.append(keys[-1])
    def deterministic_make_key(length):
        key = keys.pop()
        print "  deterministic_make_key() is returning %s" % key
        return key
    return deterministic_make_key

def run(settings, log=log, bucket='temp-hackpub-test'):
    log("initializing S3Storage with bucket %s" % bucket)

    storage = S3Storage(
        access_key_id=settings.AWS_ACCESS_KEY_ID,
        secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        bucket=bucket,
        generate_key=make_repeated_keygen()
    )

    try:
        url_0 = storage.create('hi', 'text/plain', {})
        print "created a new item at %s" % url_0

        content = u'<p>hi\u2026</p>'
        content_type = 'text/html; charset=utf-8'
        url = storage.create(content.encode('utf-8'), content_type, {
          'foo': 'bar'
        })
        print "created a new item at %s" % url
        if url == url_0:
            raise AssertionError("key collision!")
        print "fetching it..."
        resp, resp_content = storage.http.request(url)
        if resp.status != 200:
            raise AssertionError('got status %d' % resp.status)
        if resp['content-type'] != 'text/html; charset=utf-8':
            raise AssertionError('content type is %s' % resp['content-type'])
        if resp_content.decode('utf-8') != content:
            raise AssertionError('content is %s' % repr(resp_content))
        print "  it looks good!"
        key = url.split('/')[-1]
        print "fetching metadata for key %s..." % key
        metadata = storage.get_metadata(key)
        if metadata != {'foo': 'bar', 'published-url': url}:
            raise AssertionError('metadata is %s' % repr(metadata))
        print "  it looks good!"
    finally:
        print "cleaning up..."
        items = storage.conn.list_bucket(bucket)
        for item in items.entries:
            print "deleting key %s" % item.key
            storage.conn.delete(bucket, item.key)
        print "deleting bucket %s" % bucket
        storage.conn.delete_bucket(bucket)

    print "done."
