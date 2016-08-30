import docker
from .models.containers import ContainerCollection
from .models.images import ImageCollection

def from_env():
    return Client.from_env()

class Client(object):
    def __init__(self, api):
        self.api = api

    @classmethod
    def from_env(cls):
        return cls(docker.from_env())

    # Resources
    @property
    def containers(self):
        return ContainerCollection(client=self)

    @property
    def images(self):
        return ImageCollection(client=self)

    # Top-level methods
    def events(self, *args, **kwargs):
        return self.api.events(*args, **kwargs)

    def info(self, *args, **kwargs):
        return self.api.info(*args, **kwargs)

    def login(self, *args, **kwargs):
        return self.api.login(*args, **kwargs)

    def ping(self, *args, **kwargs):
        return self.api.ping(*args, **kwargs) == 'OK'

    def version(self, *args, **kwargs):
        return self.api.version(*args, **kwargs)
