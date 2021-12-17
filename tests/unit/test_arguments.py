"""
    Tests if argv arguments are passed properly.
"""

import pytest

def test_arguments(hook):
    """Verifying arguments are being kept appropriatly"""
    # Verify arguments with values
    test_args = ["dogecoind", "-maxconnections=150", "-paytxfee=0.01"]
    test_env = {
            "DATADIR" : pytest.datadir,
            }

    result_args = [
            pytest.abs_path("dogecoind"),
            f"-datadir={pytest.datadir}",
            "-maxconnections=150",
            "-paytxfee=0.01",
            "-printtoconsole",
            ]
    result_env = {}
    hook.test(test_args, test_env, result_args, result_env)
    assert hook.result == hook.reference

    # Verify arguments without values
    test_args = ["dogecoind", "-daemon", "-testnet"]
    test_env = {
            "DATADIR" : pytest.datadir,
            }

    result_args = [
            pytest.abs_path("dogecoind"),
            f"-datadir={pytest.datadir}",
            "-daemon",
            "-testnet",
            "-printtoconsole",
            ]
    result_env = {}
    hook.test(test_args, test_env, result_args, result_env)
    assert hook.result == hook.reference

    # Mixing arguments with and without values
    test_args = ["dogecoind", "-daemon", "-maxconnections=150"]
    test_env = {
            "DATADIR" : pytest.datadir,
            }

    result_args = [
            pytest.abs_path("dogecoind"),
            f"-datadir={pytest.datadir}",
            "-daemon",
            "-maxconnections=150",
            "-printtoconsole",
            ]
    result_env = {}
    hook.test(test_args, test_env, result_args, result_env)
    assert hook.result == hook.reference

def test_arguments_double_dash(hook):
    """Check arguments formates with double-dash like `--testnet`"""
    test_args = ["dogecoind", "--maxconnections=150", "--paytxfee=0.01"]
    test_env = {
            "DATADIR" : pytest.datadir,
            }

    result_args = [
            pytest.abs_path("dogecoind"),
            f"-datadir={pytest.datadir}",
            "--maxconnections=150",
            "--paytxfee=0.01",
            "-printtoconsole",
            ]
    result_env = {}
    hook.test(test_args, test_env, result_args, result_env)
    assert hook.result == hook.reference
