"""
    Command interface for os.execve hook from EntrypointHook.

    Store arguments and environ for hooked commands, used to create
    both the command of entrypoint.py called during tests,
    and the expected command for test comparison.
"""

import difflib
import json

class CommandNotFound(Exception):
    """Raised when entrypoint command is not found or test fail."""

class Command:
    """
    Represent a single execve command, with
    its arguments and environment.

    Can represent an entrypoint hooked command, the expected
    result or the input of a test.
    """
    def __init__(self, argv, environ):
        # Sort cli arguments to facilitate comparaison
        sorted_args = argv[1:]
        sorted_args.sort()

        self.argv = [argv[0]] + sorted_args
        self.environ = environ

    def __eq__(self, other):
        """Compare 2 Command, result of a test and expected command."""
        return self.argv == other.argv and self.environ == other.environ

    def __str__(self):
        """Render single command into string for error outputs."""
        argv_str = json.dumps(self.argv, indent=4)
        command_str = f"argv: {argv_str}\n"
        environ_str = json.dumps(self.environ, indent=4)
        command_str += f"environ: {environ_str}"
        return command_str

    def diff(self, other):
        """Perform diff between result command and expected command."""
        command = str(self).splitlines()
        other_command = str(other).splitlines()

        return difflib.unified_diff(command, other_command,
                fromfile="result", tofile="expected", lineterm="")
