"""
    Pytest configuration file for tests fixtures, global variables
    and error messages for tests errors.

    Pytest fixtures are used to arrange and clean up tests environment.
    See: https://docs.pytest.org/en/6.2.x/fixture.html
"""

import os
import tempfile
import pytest
from hooks.entrypoint_hook import EntrypointHook
from hooks.command import Command

def abs_path(executable):
    """Format expected location of dogecoin executables in containers"""
    return os.path.join(pytest.executables_folder, executable)

def pytest_configure():
    """Declare global variables to use across tests"""
    # User used for tests
    pytest.user = os.environ["USER"]

    # Perform tests in a temporary directory, used as datadir
    pytest.directory = tempfile.TemporaryDirectory()
    pytest.datadir = pytest.directory.name

    # Location where dogecoin executables should be located
    pytest.executables_folder = "/usr/local/bin"
    pytest.abs_path = abs_path

@pytest.fixture
def hook():
    """
    Prepare & cleanup EntrypointHook for tests, by disabling and restoring
    entrypoint functions & system calls.

    EntrypointHook.test is then used inside a test, available as hook.test.
    """
    test_hook = EntrypointHook()
    yield test_hook
    test_hook.reset_hooks()

def pytest_assertrepr_compare(left, right):
    """Override error messages of AssertionError on test failure."""
    # Display comparison of result command and an expected execve command
    if isinstance(left, Command) and isinstance(right, Command):
        assert_msg = ["fail"]
        assert_msg.append("======= Result =======")
        assert_msg.extend(str(left).splitlines())
        assert_msg.append("======= Expected =======")
        assert_msg.extend(str(right).splitlines())
        assert_msg.append("======= Diff =======")
        assert_msg.extend(left.diff(right))
        return assert_msg
    return None
