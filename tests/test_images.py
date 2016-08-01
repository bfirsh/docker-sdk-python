import dockersdk
import unittest

class ImageTest(unittest.TestCase):
    def test_pull(self):
        client = dockersdk.from_env()
        image = client.images.pull('alpine:latest')
        assert 'alpine:latest' in image.attrs['RepoTags']

    def test_list(self):
        client = dockersdk.from_env()
        image = client.images.pull('alpine:latest')
        assert image.id in map(lambda i: i.id, client.images.list())
