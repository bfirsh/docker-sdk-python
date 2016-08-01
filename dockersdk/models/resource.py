
class Model(object):
    def __init__(self, attrs=None, url=None, api_client=None, collection=None):
        self.url = url
        self.api_client = api_client
        self.collection = collection
        self.attrs = attrs
        if self.attrs is None:
            self.attrs = {}

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.short_id)

    @property
    def id(self):
        return self.attrs.get("Id")

    @property
    def short_id(self):
        return self.id[:10]


class Collection(object):
    def __init__(self, api_client=None, url=None):
        self.api_client = api_client
        self.url = url

    def list(self):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def create(self, attrs=None):
        raise NotImplementedError

    def delete(self, model):
        raise NotImplementedError

    def prepare_model(self, attrs):
        if isinstance(attrs, Model):
            attrs.api_client = self.api_client
            attrs.collection = self
            return attrs
        elif isinstance(attrs, dict):
            return self.model(attrs=attrs, api_client=self.api_client, collection=self)
        else:
            raise Exception("Can't create %s from %s" % (self.model.__name__, attrs))
