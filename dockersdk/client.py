import docker
from .models.containers import ContainerCollection
from .models.images import ImageCollection

def from_env():
    return Client.from_env()

class Client(object):
    def __init__(self, api_client):
        self.api_client = api_client

    @classmethod
    def from_env(cls):
        return cls(docker.from_env())

    # Resources
    @property
    def containers(self):
        return ContainerCollection(api_client=self.api_client)

    @property
    def images(self):
        return ImageCollection(api_client=self.api_client)

    # Top-level methods
    def events(self, *args, **kwargs):
        return self.api_client.events(*args, **kwargs)

    def info(self, *args, **kwargs):
        return self.api_client.info(*args, **kwargs)

    def login(self, *args, **kwargs):
        return self.api_client.login(*args, **kwargs)

    def ping(self, *args, **kwargs):
        return self.api_client.ping(*args, **kwargs) == 'OK'

    def version(self, *args, **kwargs):
        return self.api_client.version(*args, **kwargs)
