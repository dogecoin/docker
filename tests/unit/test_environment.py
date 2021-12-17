"""
    Tests if environment variable alone are converted into
    arguments by entrypoint.
"""

import pytest

def test_environment(hook):
    """
    Verify if environment is converted to arguments,
    control that arguments are removed from the environment.
    """
    # Control environment variables with values
    test_args = ["dogecoind"]
    test_env = {
            "DATADIR" : pytest.datadir,
            "MAXCONNECTIONS" : "150",
            "PAYTXFEE" : "0.01"
            }

    result_args = [
            pytest.abs_path("dogecoind"),
            f"-datadir={pytest.datadir}",
            "-paytxfee=0.01",
            "-maxconnections=150",
            "-printtoconsole",
            ]
    result_env = {}
    hook.test(test_args, test_env, result_args, result_env)
    assert hook.result == hook.reference

    # Control environment variables with empty values
    test_env = {
            "DATADIR" : pytest.datadir,
            "TESTNET" : "",
            "DAEMON" : "",
            }

    result_args = [
            pytest.abs_path("dogecoind"),
            "-daemon",
            f"-datadir={pytest.datadir}",
            "-testnet",
            "-printtoconsole",
            ]
    result_env = {}
    hook.test(test_args, test_env, result_args, result_env)
    assert hook.result == hook.reference
