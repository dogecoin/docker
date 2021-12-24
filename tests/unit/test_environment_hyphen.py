"""
    Tests environment variables containing an hyphen (-).

    Special case for environment conversion.
"""

import pytest

def test_environment_hyphen(hook):
    """
    Test option with dash like `-help-debug` if working
    properly in environment.
    """
    test_args = ["dogecoind"]
    test_env = {
            "DATADIR" : pytest.datadir,
            "HELP_DEBUG" : "",
            }

    result_args = [
            pytest.abs_path("dogecoind"),
            f"-datadir={pytest.datadir}",
            "-help-debug",
            "-printtoconsole",
            ]
    result_env = {}
    hook.test(test_args, test_env, result_args, result_env)
    assert hook.result == hook.reference
