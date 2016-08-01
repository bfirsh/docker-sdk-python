class ContainerError(Exception):
    def __init__(self, container, exit_status, command, image, stderr):
        self.container = container
        self.exit_status = exit_status
        self.command = command
        self.image = image
        self.stderr = stderr
        msg = "Command '{}' in image '{}' returned non-zero exit status {}: {}".format(command, image, exit_status, stderr)
        super(ProcessError, self).__init__(msg)
