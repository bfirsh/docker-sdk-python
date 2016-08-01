import docker
from .models.containers import ContainerCollection

def from_env():
    return Client.from_env()

class Client(object):
    def __init__(self, api_client):
        self.api_client = api_client

    @classmethod
    def from_env(cls):
        return cls(docker.from_env())

    @property
    def container(self):
        return ContainerCollection(api_client=self.api_client)
