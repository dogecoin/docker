#!/usr/bin/env python3
# Copyright (c) 2021 The Dogecoin Core developers
"""
    Tests metadatas of files provided by the Dockerfile.
"""

import os

from .framework.test_runner import TestRunner

class FilesMetadataTest(TestRunner):
    """Verification of container files' metadata"""

    def __init__(self):
        TestRunner.__init__(self)

    def add_options(self, parser):
        """Extra options for the test"""

    def run_test(self):
        """
        Verifiy availability and metadata of all files provided by the image,
        check user, group and mode.
        """
        location = "/usr/local/bin/"

        abs_path = lambda executable : os.path.join(location, executable)

        dogecoind = self.container_file(abs_path("dogecoind"))
        assert dogecoind.user == "dogecoin"
        assert dogecoind.group == "dogecoin"
        assert dogecoind.mode == "4555"

        dogecointx = self.container_file(abs_path("dogecoin-tx"))
        assert dogecointx.user == "dogecoin"
        assert dogecointx.group == "dogecoin"
        assert dogecointx.mode == "4555"

        dogecoincli = self.container_file(abs_path("dogecoin-cli"))
        assert dogecoincli.user == "dogecoin"
        assert dogecoincli.group == "dogecoin"
        assert dogecoincli.mode == "4555"

        entrypoint = self.container_file(abs_path("entrypoint.py"))
        assert entrypoint.user == "root"
        assert entrypoint.group == "root"
        assert entrypoint.mode == "500"

if __name__ == '__main__':
    FilesMetadataTest().main()
