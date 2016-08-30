from docker.errors import APIError
from ..errors import ContainerError
from ..utils import dict_filter
from .resource import Collection, Model

CREATE_KWARGS = ["hostname", "user", "detach", "stdin_open", "tty", "mem_limit", "ports", "environment", "dns", "volumes", "volumes_from", "network_disabled", "name", "entrypoint", "cpu_shares", "working_dir", "domainname", "memswap_limit", "cpuset", "host_config", "mac_address", "labels"]

START_KWARGS = ["binds", "port_bindings", "lxc_conf", "publish_all_ports", "links", "privileged", "dns", "dns_search", "volumes_from", "network_mode", "restart_policy", "cap_add", "cap_drop", "devices", "extra_hosts", "read_only", "pid_mode", "ipc_mode", "security_opt", "ulimits"]


class Container(Model):
    @property
    def status(self):
        """
        Returns the status of the container. For example, `running` or `exited`.
        """
        return self.attrs['State']['Status']

    def attach(self, *args, **kwargs):
        return self.client.api.attach(self.id, *args, **kwargs)

    def commit(self, *args, **kwargs):
        # TODO return image
        return self.client.api.commit(self.id, *args, **kwargs)

    def diff(self, *args, **kwargs):
        return self.client.api.diff(self.id, *args, **kwargs)

    def export(self, *args, **kwargs):
        return self.client.api.export(self.id, *args, **kwargs)

    def get_archive(self, *args, **kwargs):
        return self.client.api.get_archive(self.id, *args, **kwargs)

    def kill(self, *args, **kwargs):
        return self.client.api.kill(self.id, *args, **kwargs)

    def logs(self, *args, **kwargs):
        return self.client.api.logs(self.id, *args, **kwargs)

    def pause(self, *args, **kwargs):
        return self.client.api.pause(self.id, *args, **kwargs)

    def put_archive(self, *args, **kwargs):
        return self.client.api.put_archive(self.id, *args, **kwargs)

    def remove(self, *args, **kwargs):
        return self.client.api.remove_container(self.id, *args, **kwargs)

    def rename(self, *args, **kwargs):
        return self.client.api.rename(self.id, *args, **kwargs)

    def resize(self, *args, **kwargs):
        return self.client.api.resize(self.id, *args, **kwargs)

    def restart(self, *args, **kwargs):
        return self.client.api.restart(self.id, *args, **kwargs)

    def start(self, *args, **kwargs):
        return self.client.api.start(self.id, *args, **kwargs)

    def stats(self, *args, **kwargs):
        return self.client.api.stats(self.id, *args, **kwargs)

    def stop(self, *args, **kwargs):
        return self.client.api.stop(self.id, *args, **kwargs)

    def top(self, *args, **kwargs):
        return self.client.api.top(self.id, *args, **kwargs)

    def update(self, *args, **kwargs):
        return self.client.api.update(self.id, *args, **kwargs)

    def wait(self, *args, **kwargs):
        return self.client.api.wait(self.id, *args, **kwargs)


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
        resp = self.client.api.create_container(*args, **kwargs)
        return self.get(resp['Id'])

    def get(self, cid):
        return self.prepare_model(self.client.api.inspect_container(cid))

    def list(self, *args, **kwargs):
        return [
            self.get(r['Id'])
            for r in self.client.api.containers(*args, **kwargs)
        ]
