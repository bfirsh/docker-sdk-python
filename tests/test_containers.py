import dockersdk
import unittest

class ContainerTest(unittest.TestCase):
    def test_run(self):
        client = dockersdk.from_env()
        self.assertEqual(
            client.containers.run("alpine", "echo hello world"),
            b'hello world\n'
        )

    def test_run_detach(self):
        client = dockersdk.from_env()
        container = client.containers.run("alpine", "sleep 300", detach=True)
        assert container.attrs['Config']['Image'] == "alpine"
        assert container.attrs['Config']['Cmd'] == ['sleep', '300']

    def test_get(self):
        client = dockersdk.from_env()
        container = client.containers.run("alpine", "sleep 300", detach=True)
        assert client.containers.get(container.id).attrs['Config']['Image'] == "alpine"

    def test_list(self):
        client = dockersdk.from_env()
        container_id = client.containers.run("alpine", "sleep 300", detach=True).id
        containers = [c for c in client.containers.list() if c.id == container_id]
        assert len(containers) == 1

        container = containers[0]
        assert container.attrs['Config']['Image'] == 'alpine'

        container.kill()
        container.remove()
        assert container_id not in [c.id for c in client.containers.list()]
