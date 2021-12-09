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
        """Make sure there is an options object"""
        self.options = {}

    def add_options(self, parser):
        """Allow adding options in tests"""

    def run_test(self):
        """Actual test, must be implemented by the final class"""
        raise NotImplementedError

    def run_command(self, envs, args):
        """Run a docker command with env and args"""
        assert self.options.platform is not None
        assert self.options.image is not None

        runner = DockerRunner(self.options.platform,
            self.options.image, self.options.verbose)

        return runner.run_interactive_command(envs, args)

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

        self.run_test()
        print("Tests successful")
        sys.exit(0)
