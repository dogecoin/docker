#!/usr/bin/env python3
# Copyright (c) 2021 The Dogecoin Core developers
"""
Base class to define and run Dogecoin Core Docker tests with
"""

import argparse
import sys

from .docker_runner import DockerRunner

class TestConfigurationError(Exception):
    """Raised when the test is configured inconsistently"""

class TestRunner:
    """Base class to define and run Dogecoin Core Docker tests with"""
    def __init__(self):
        self.options = {}
        self.container = None

    def add_options(self, parser):
        """Allow adding options in tests"""

    def run_test(self):
        """Actual test, must be implemented by the final class"""
        raise NotImplementedError

    def docker_exec(self, envs, args):
        """
        Launch `docker exec` command, run command inside a background container.
        Let execute mutliple instructions in the same container.
        """
        assert self.options.platform is not None
        assert self.options.image is not None

        return self.container.execute(envs, args)

    def docker_run(self, envs, args):
        """Launch `docker run` command, create a new container for each run"""
        assert self.options.platform is not None
        assert self.options.image is not None

        return self.container.run(envs, args)

    def main(self):
        """main loop"""
        parser = argparse.ArgumentParser()
        parser.add_argument("--platform", dest="platform", required=True,
            help="The platform to use for testing, eg: 'linux/amd64'")
        parser.add_argument("--image", dest="image", required=True,
            help="The image or tag to execute tests against, eg: 'verywowimage'")
        parser.add_argument("--verbose", dest="verbose", default=False, action="store_true",
            help="Verbosely output actions taken and print docker logs, regardless of outcome")

        self.add_options(parser)
        self.options = parser.parse_args()

        self.container = DockerRunner(self.options.platform,
                self.options.image, self.options.verbose)

        self.run_test()
        print("Tests successful")
        sys.exit(0)
