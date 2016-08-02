import dockersdk
import unittest

class ContainerTest(unittest.TestCase):
    def test_run(self):
        client = dockersdk.from_env()
        self.assertEqual(
            client.container.run("alpine", "echo hello world"),
            b'hello world\n'
        )

    def test_get(self):
        client = dockersdk.from_env()
        container = client.container.run("alpine", "sleep 300", detach=True)
        assert client.container.get(container.id).attrs['Config']['Image'] == "alpine"

    def test_list(self):
        client = dockersdk.from_env()
        container = client.container.run("alpine", "sleep 300", detach=True)
        assert container.id in map(lambda c: c.id, client.container.list())
        container.kill()
        container.remove()
        assert container.id not in map(lambda c: c.id, client.container.list())
