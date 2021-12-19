#!/usr/bin/env python3
# Copyright (c) 2021 The Dogecoin Core developers
"""
Test framework for end-to-end docker tests
"""

import subprocess
import sys

class DockerRunner:
    """
    Interface with the Docker cli to build & launch `docker run` and
    `docker exec` commands.

    - `docker run` is used for a one shot container.
    - `docker exec` enable a test to use the same background container for
      multiples commands, launched automatically at first exec instruction.
    """
    def __init__(self, platform, image, verbose):
        """Sets platform and image for all tests ran with this instance"""
        self.platform = platform
        self.image = image
        self.verbose = verbose
        #Background container for `docker exec`
        self.container_id = None

    def execute(self, envs, args):
        """Launch `docker exec` commands inside the background container"""
        # Create background container if not existing on first exec command
        if self.container_id is None:
            self._start_background()

        command = self._construct_command("exec", envs, args)
        return self._shell(command)

    def run(self, envs, args):
        """
        Launch `docker run` commands to create a new container for each command
        """
        command = self._construct_command("run", envs, args)
        return self._shell(command)

    def __del__(self):
        """Clean up background container if enabled"""
        self._stop_background()

    def _start_background(self):
        """
        Launch a docker container. Done in 2 step using create + start.

        Keep the container running with a shell open thanks to `--interactive`,
        having stdin open keep the process running.
        """
        create_command = [
                "docker", "create",
                "--platform", self.platform,
                "--interactive",
                self.image,
                "/bin/bash",
                ]
        self.container_id = self._shell(create_command, silent=True)

        start_command = [
                "docker", "start", self.container_id
                ]
        self._shell(start_command, silent=True)

    def _stop_background(self):
        """Remove background test container if used"""
        stop_command = ["docker", "rm", "-f", self.container_id]
        if self.container_id:
            self._shell(stop_command, silent=True)

    def _shell(self, command, silent=False):
        """Run an arbitrary shell command and return its output"""
        if self.verbose and not silent:
            print(f"$ { ' '.join(command) }")

        try:
            result = subprocess.run(command, capture_output=True, check=True)
        except subprocess.CalledProcessError as command_err:
            print(command_err.stdout.decode("utf-8"), file=sys.stdout)
            print(command_err.stderr.decode("utf-8"), file=sys.stderr)
            raise command_err

        return result.stdout.decode("utf-8").strip()

    def _construct_command(self, docker_cmd, envs, args):
        """Construct a docker command with env and args"""
        command = ["docker", docker_cmd]

        for env in envs:
            command.append("-e")
            command.append(env)

        # Use container or image depending on command type
        if docker_cmd == "exec":
            tag = self.container_id
        elif docker_cmd == "run":
            tag = self.image

        command.append(tag)

        # Launch all shell commands using entrypoint.py only
        command.append("entrypoint.py")

        # Need to add a default executables added by CMD normally
        if len(args) == 0 or args[0].startswith("-"):
            command.append("dogecoind")

        command.extend(args)

        return command
