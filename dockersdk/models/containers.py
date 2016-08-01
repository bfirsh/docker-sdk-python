from docker.errors import APIError
from ..errors import ContainerError
from ..utils import dict_filter
from .resource import Collection, Model

CREATE_KWARGS = ["hostname", "user", "detach", "stdin_open", "tty", "mem_limit", "ports", "environment", "dns", "volumes", "volumes_from", "network_disabled", "name", "entrypoint", "cpu_shares", "working_dir", "domainname", "memswap_limit", "cpuset", "host_config", "mac_address", "labels"]

START_KWARGS = ["binds", "port_bindings", "lxc_conf", "publish_all_ports", "links", "privileged", "dns", "dns_search", "volumes_from", "network_mode", "restart_policy", "cap_add", "cap_drop", "devices", "extra_hosts", "read_only", "pid_mode", "ipc_mode", "security_opt", "ulimits"]

class Container(Model):
    def start(self, *args, **kwargs):
        return self.api_client.start(self.id, *args, **kwargs)

    def logs(self, *args, **kwargs):
        return self.api_client.logs(self.id, *args, **kwargs)

    def wait(self, *args, **kwargs):
        return self.api_client.wait(self.id, *args, **kwargs)

    def kill(self, *args, **kwargs):
        return self.api_client.kill(self.id, *args, **kwargs)

    def remove(self, *args, **kwargs):
        return self.api_client.remove_container(self.id, *args, **kwargs)

class ContainerCollection(Collection):
    model = Container

    def run(self, image, command=None, stdout=True, stderr=False, **kwargs):
        create_kwargs = dict_filter(kwargs, CREATE_KWARGS)
        detach = kwargs.get("detach", False)
        try:
            container = self.create(image, command, **create_kwargs)
        except APIError as e:
            raise # TODO

        start_kwargs = dict_filter(kwargs, START_KWARGS)
        container.start(**start_kwargs)

        if detach:
            return container

        exit_status = container.wait()
        if exit_status != 0:
            raise ContainerError(
                container,
                exit_status,
                command,
                image,
                container.logs(stdout=False, stderr=True)
            )
        return container.logs(stdout=stdout, stderr=stderr)

    def create(self, *args, **kwargs):
        return self.prepare_model(self.api_client.create_container(*args, **kwargs))

    def list(self):
        return [
            self.prepare_model(r)
            for r in self.api_client.containers()
        ]
