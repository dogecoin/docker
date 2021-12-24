"""
    Hook for tests of entrypoint.py behavior. Abstract functions and system
    call to catch arguments used by entrypoint, or disable unwanted functions.

    EntrypointHook.test is used to perform a single test by
    calling entrypoint.main. The hook is available as a test fixture, inside
    a test argument.

    Test example:

    def test_for_entrypoint(hook):
        # Values to test
        test_argv = [value1, ...]
        test_env = {key:value, ...}

        # Expected result
        result_argv = [value1, ...]
        result_env = {key:value, ...}

        # Perform the test using the hook
        hook.test(test_argv, test_env, result_argv, result_env)
        assert hook.result == hook.reference

    Visit also pytest doc for test formatting: https://docs.pytest.org/
"""

import sys
import os
import shutil
import entrypoint
import hooks.help_menus
from hooks.command import Command, CommandNotFound

class EntrypointHook:
    """
    Hook to perform tests of the Dockerfile entrypoint.py. Manage all
    informations about test result and expected output for test comparison.

    Hook some system calls & functions used by `entrypoint.main` to handle
    commands which should have been run by the script.
    Disable some function related so file permissions & creation.

    See `self._setup_hooks` for all defined hooks.
    """
    # Environment to use for every tests Command & comparison Command
    DEFAULT_ENV = {
        "USER" : os.environ["USER"],
        "PATH" : os.environ["PATH"],
            }

    def __init__(self):
        self.result = None
        self.reference = None

        self._setup_hooks()

    def test(self, test_argv, test_environ, \
            result_argv, result_environ):
        """
        Run a test of entrypoint.main and store expected result in the hook
        for further comparaison.

        - self.result store entrypoint.py command launched by main
        - self.reference store the expected Command for comparison.

        Stored Command objects are comparable, used for asserts.
        Example:
        >>> assert hook.result == hook.reference
        """
        # Clean hook from previous test, store the command to test
        self._reset_attributes()

        # Default environment variables needed by all tests
        test_environ.update(self.DEFAULT_ENV)
        result_environ.update(self.DEFAULT_ENV)

        # Manage system arguments & environment used by the script
        sys.argv[1:] = test_argv.copy()
        os.environ = test_environ.copy()

        # Run the test, launching entrypoint script from the main
        entrypoint.main()

        # Store expected Command used for comparison
        self.reference = Command(result_argv, result_environ)

        if self.result is None:
            raise CommandNotFound("Test fail, do not return a command")

    def _execve_hook(self, executable, argv, environ):
        """
        Hook for os.execve function, to catch arguments/environment
        instead of launching processes.
        """
        assert executable == argv[0]
        self.result = Command(argv, environ)

    @staticmethod
    def _get_help_hook(command_arguments):
        """
        Hook call of executable help menu to retrieve options.
        Fake a list of raw options generated by entrypoint.get_help.
        """
        executable = command_arguments[0]

        #Test use of -help-debug to expand help options
        if executable == "dogecoind":
            assert "-help-debug" in command_arguments
        else:
            assert "-help-debug" not in command_arguments
        return getattr(hooks.help_menus, executable.replace("-", "_"))

    def _reset_attributes(self):
        """Clean state between each test"""
        self.result = None
        self.reference = None

    def _setup_hooks(self):
        """
        Enable hooks of entrypoint.py system & functions calls, disable
        some functions.

        Replace entrypoint function by EntrypointHook methods
        to handle arguments used by entrypoint calls.

        Save references to previous functions to restore them test
        clean up.
        """
        # Save hooked functions for restoration
        self._execve_backup = os.execve
        self._setgid_backup = os.setgid
        self._setuid_backup = os.setuid
        self._which_backup = shutil.which
        self._get_help_backup = entrypoint.get_help

        # Setup hooks
        # Add execve hook globally to catch entrypoint arguments
        os.execve = self._execve_hook
        # Hook executables call to `-help` menus to fake options
        entrypoint.get_help = self._get_help_hook

        # which not working from host without dogecoin executables in PATH
        shutil.which = lambda executable : f"/usr/local/bin/{executable}"

        # Disable setgid & setuid behavior
        os.setgid = lambda _ : None
        os.setuid = lambda _ : None

    def reset_hooks(self):
        """Restore hooks of `self._setup_hooks` to initial functions"""
        os.execve = self._execve_backup
        os.setgid = self._setgid_backup
        os.setuid = self._setuid_backup
        shutil.which = self._which_backup
        entrypoint.get_help = self._get_help_backup
