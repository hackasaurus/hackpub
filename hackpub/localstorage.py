import mimetypes

class LocalStorage(object):
    def __init__(self, root):
        self.root = root

    def get_metadata(self, key):
        # We don't support this.
        return None

    def create(self, content, mimetype, metadata):
        dotted_ext = mimetypes.guess_extension(mimetype)

        # TODO: Finish this.
