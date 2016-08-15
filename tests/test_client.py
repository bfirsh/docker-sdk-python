import dockersdk
import unittest

class ClientTest(unittest.TestCase):
    def test_events(self):
        pass

    def test_info(self):
        client = dockersdk.from_env()
        info = client.info()
        assert 'ID' in info
        assert 'Name' in info

    def test_login(self):
        pass

    def test_ping(self):
        client = dockersdk.from_env()
        assert client.ping() is True

    def test_version(self):
        client = dockersdk.from_env()
        assert 'Version' in client.version()
