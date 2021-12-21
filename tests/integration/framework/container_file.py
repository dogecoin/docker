"""
    Base class to store metadatas of container files.
"""

class ContainerFile:
    """
    File interface to inspects metadatas of container files.

    Run shell command (self.command) and store container output.
    """
    command = "stat"
    # format: <name> <user>:<group> <mode>
    format = "%n %U:%G %a"

    def __init__(self, name, container_cli):
        self.name = name
        self.user = None
        self.group = None
        self.mode = None

        # Retrieve file information inside the container
        file_info = container_cli([], self.shell_command())

        # Convert raw container output to class attributes
        self.convert_output(file_info.stdout.decode("utf-8"))

    def shell_command(self):
        """Format the container command to retrieve file metadata"""
        return [self.command, self.name, "-c", self.format]

    def convert_output(self, stat_output):
        """
        Clean up container output about file metadatas. Convert
        informations into ContainerFile attributes.

        Conversion follow self.format.
        """
        stat_output = stat_output.strip()
        _, user_info, mode = stat_output.split(" ")
        self.mode = mode
        self.user, self.group = user_info.split(":")

    def __str__(self):
        return f"{self.name} {self.user}:{self.group} {self.mode}"
