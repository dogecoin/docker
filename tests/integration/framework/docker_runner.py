#!/usr/bin/env python3
# Copyright (c) 2021 The Dogecoin Core developers
"""
Test framework for end-to-end docker tests
"""

import subprocess
import sys

class DockerRunner:
    """Run docker containers for testing"""

    def __init__(self, platform, image, verbose):
        """Sets platform and image for all tests ran with this instance"""
        self.platform = platform
        self.image = image
        self.verbose = verbose

    def construct_docker_command(self, envs, args):
        """
        Construct a docker command with env and args
        """
        command = ["docker", "run", "--platform", self.platform]

        for env in envs:
            command.append("-e")
            command.append(env)

        command.append(self.image)

        for arg in args:
            command.append(arg)

        return command

    def run_interactive_command(self, envs, args):
        """
        Run our target docker image with a list of
        environment variables and a list of arguments
        """
        command = self.construct_docker_command(envs, args)

        if self.verbose:
            print(f"Running command: { ' '.join(command) }")

        try:
            output = subprocess.run(command, capture_output=True, check=True)
        except subprocess.CalledProcessError as docker_err:
            print(f"Error while running command: { ' '.join(command) }", file=sys.stderr)
            print(docker_err, file=sys.stderr)
            print(docker_err.stderr.decode("utf-8"), file=sys.stderr)
            print(docker_err.stdout.decode("utf-8"), file=sys.stdout)

            raise docker_err

        return output
