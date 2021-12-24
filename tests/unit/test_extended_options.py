"""
    Tests if extended help menus are available as environment variables.

    Control if options from `-help-debug` are available.
"""

import pytest

def test_extended_options(hook):
    """Verify dogecoind environment variables from `-help-debug` options"""
    test_args = ["dogecoind"]
    test_env = {
            "DATADIR" : pytest.datadir,
            "REGTEST" : "1",
            "SENDFREETRANSACTIONS" : "",
            "CHECKBLOCKS":"420",
            }

    result_args = [
            pytest.abs_path("dogecoind"),
            f"-datadir={pytest.datadir}",
            "-sendfreetransactions",
            "-checkblocks=420",
            "-regtest=1",
            "-printtoconsole",
            ]
    result_env = {}
    hook.test(test_args, test_env, result_args, result_env)
    assert hook.result == hook.reference

def test_invalid_extended(hook):
    """Control `-help-debug` options not extended with other executables"""
    test_args = ["dogecoin-cli"]
    test_env = {
            "DATADIR" : pytest.datadir,
            "SENDFREETRANSACTIONS" : "",
            "CHECKBLOCKS":"420",
            }

    result_args = [
            pytest.abs_path("dogecoin-cli"),
            f"-datadir={pytest.datadir}",
            ]
    result_env = {
            "SENDFREETRANSACTIONS" : "",
            "CHECKBLOCKS":"420",
            }
    hook.test(test_args, test_env, result_args, result_env)
    assert hook.result == hook.reference
