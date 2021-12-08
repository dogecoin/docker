#!/usr/bin/env python3
# Copyright (c) 2021 The Dogecoin Core developers
"""
Test the version installed to be the expected version
"""

import re

from .framework.test_runner import TestRunner

class VersionTest(TestRunner):
    """Versions test"""

    def __init__(self):
        """Constructor"""
        TestRunner.__init__(self)
        self.version_expr = None

    def add_options(self, parser):
        """Add test-specific --version option"""
        parser.add_argument("--version", dest="version", required=True,
            help="The version that is expected to be installed, eg: '1.14.5'")

    def run_test(self):
        """Check the version of each executable"""

        self.version_expr = re.compile(f".*{ self.options.version }.*")

        # check dogecoind with only env
        dogecoind = self.run_command(["VERSION=1"], [])
        self.ensure_version_on_first_line(dogecoind.stdout)

        # check dogecoin-cli
        dogecoincli = self.run_command([], ["dogecoin-cli", "-?"])
        self.ensure_version_on_first_line(dogecoincli.stdout)

        # check dogecoin-tx
        dogecointx = self.run_command([], ["dogecoin-tx", "-?"])
        self.ensure_version_on_first_line(dogecointx.stdout)

        # make sure that we find version errors
        caught_error = False
        try:
            self.ensure_version_on_first_line("no version here".encode('utf-8'))
        except AssertionError:
            caught_error = True

        if not caught_error:
            raise AssertionError("Failed to catch a missing version")

    def ensure_version_on_first_line(self, cmd_output):
        """Assert that the version is contained in the first line of output string"""
        first_line = cmd_output.decode("utf-8").split("\n")[0]

        if re.match(self.version_expr, first_line) is None:
            text = f"Could not find version { self.options.version } in { first_line }"
            raise AssertionError(text)

if __name__ == '__main__':
    VersionTest().main()
