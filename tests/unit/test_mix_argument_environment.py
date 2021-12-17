"""
    Tests formatting of commands using environment variables + arguments.
"""

import pytest

def test_mixing_argument_and_env(hook):
    """Configure container with arguments and environment variables"""
    test_args = ["dogecoind", "-maxconnections=150", "-daemon"]
    test_env = {
            "DATADIR" : pytest.datadir,
            "TESTNET" : "",
            }

    result_args = [
            pytest.abs_path("dogecoind"),
            f"-datadir={pytest.datadir}",
            "-maxconnections=150",
            "-daemon",
            "-testnet",
            "-printtoconsole",
            ]
    result_env = {}
    hook.test(test_args, test_env, result_args, result_env)
    assert hook.result == hook.reference

def test_equal_argv_and_env(hook):
    """Check arguments and environment with identical variables"""
    test_args = ["dogecoind", "-maxconnections=150", "-daemon"]
    test_env = {
            "DATADIR" : pytest.datadir,
            "MAXCONNECTIONS" : "150",
            "DAEMON" : "",
            }

    result_args = [
            pytest.abs_path("dogecoind"),
            f"-datadir={pytest.datadir}",
            "-maxconnections=150",
            "-maxconnections=150",
            "-daemon",
            "-daemon",
            "-printtoconsole",
            ]
    result_env = {}
    hook.test(test_args, test_env, result_args, result_env)
    assert hook.result == hook.reference

    #Same variable with different value for env & arguments.
    test_args = ["dogecoind", "-maxconnections=130", "-daemon"]
    test_env = {
            "DATADIR" : pytest.datadir,
            "MAXCONNECTIONS" : "150",
            "DAEMON" : "1",
            }

    result_args = [
            pytest.abs_path("dogecoind"),
            f"-datadir={pytest.datadir}",
            "-maxconnections=130",
            "-maxconnections=150",
            "-daemon",
            "-daemon=1",
            "-printtoconsole",
            ]
    result_env = {}
    hook.test(test_args, test_env, result_args, result_env)
    assert hook.result == hook.reference
