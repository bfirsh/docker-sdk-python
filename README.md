# Docker SDK for Python

A Python library for the Docker API. It lets you do anything the `docker` command does, but from within Python apps – run containers, manage containers, manage Swarms, etc.

## Installation

The latest stable version [is available on PyPi](https://pypi.python.org/pypi/docker/). Either add `docker` to your `requirements.txt` file or install with pip:

    pip install docker

## Usage

Connect to Docker using the default socket or the configuration in your environment:

```python
import docker
client = docker.from_env()
```

You can run containers:

```python
>>> client.containers.run("ubuntu", "echo hello world")
'hello world\n'
```

You can run containers in the background:

```python
>>> client.containers.run("ubuntu", "tasks/reticulate-splines", detach=True)
<Container '45e6d2de7c54'>
```

You can manage containers:

```python
>>> client.containers.list()
[<Container '45e6d2de7c54'>, <Container 'db18e4f20eaa'>, ...]

>>> container = client.containers.get('45e6d2de7c54')

>>> container.config['Cmd']
["tasks/reticulate-splines"]

>>> container.logs()
"Reticulating spline 1...\n"

>>> container.stop()
```

You can stream logs:

```python
>>> for line in container.logs(stream=True):
...   print line
Reticulating spline 2...
Reticulating spline 3...
...
```

You can manage images:

```python
>>> client.images.pull('nginx')
<Image 'nginx'>

>>> client.images.list()
[<Image 'ubuntu'>, <Image 'nginx'>, ...]
```

[Read the full documentation](https://docs.docker.com/sdk/python/) to see everything you can do.
