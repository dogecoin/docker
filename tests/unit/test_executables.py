"""
    Test if executables are found properly by entrypoint.
"""

import pytest

def test_entrypoint_executables(hook):
    """
    Basic test without configuration to check
    if entrypoint run each dogecoin executables.
    """
    # Constant variable for test
    test_environ = {
        "DATADIR" : pytest.datadir,
            }

    result_environ = {}

    # Test basic command with `dogecoind`
    test_args = ["dogecoind"]

    result_args = [
            pytest.abs_path("dogecoind"),
            f"-datadir={pytest.datadir}",
            "-printtoconsole",
            ]
    hook.test(test_args, test_environ, result_args, result_environ)
    assert hook.result == hook.reference

    # Test empty command with `dogecoin-cli`
    test_args = ["dogecoin-cli"]

    result_args = [
            pytest.abs_path("dogecoin-cli"),
            f"-datadir={pytest.datadir}",
            ]

    hook.test(test_args, test_environ, result_args, result_environ)
    assert hook.result == hook.reference

    # Test basic command with `dogecoin-tx`
    tx_result_env = {
        "DATADIR" : pytest.datadir,
            }

    test_args = ["dogecoin-tx"]

    result_args = [
            pytest.abs_path("dogecoin-tx"),
            ]
    hook.test(test_args, test_environ, result_args, tx_result_env)
    assert hook.result == hook.reference
