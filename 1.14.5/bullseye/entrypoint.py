#!/usr/bin/env python3
"""
  Docker entrypoint for Dogecoin Core
"""
import argparse
import os
import pwd
import shutil
import sys
import subprocess

CLI_EXECUTABLES = [
        "dogecoind",
        "dogecoin-cli",
        "dogecoin-tx",
        ]

def execute(executable, args):
    """
    Run container command with execve(2). Use manually execve
    to run the process as same pid and avoid to fork a child.
    """
    executable_path = shutil.which(executable)

    if executable_path is None:
        print(f"{sys.argv[0]}: {executable} not found.", file=sys.stderr)
        return 1

    #Prepare execve args & launch container command
    execve_args = [executable_path] + args
    return os.execve(executable_path, execve_args, os.environ)

def get_help(command_arguments):
    """Call any dogecoin executable help menu, retrieve its options"""
    #Prepare menu call & grep command to pipe in a shell
    menu_command = " ".join(command_arguments)
    grep_command = "grep -E '^  -[a-z]+'"

    #Return a list of raw options of `-help` output
    return subprocess.check_output(
            f"{menu_command} | {grep_command}",
            shell=True
            ).decode("utf8").splitlines()

def executable_options(executable):
    """
    Retrieve available options of a dogecoin executable using help menu.

    Call executable with `-help` flag and parse output to detect available
    Dogecoin Core options.
    """
    command_arguments = [executable, "-help"]

    #`-help-debug` display extra flag in help menu for dogecoind & qt
    if executable == "dogecoind":
        command_arguments.append("-help-debug")

    help_options = get_help(command_arguments)

    #Clean raw option from the menu, keeping only variable name.
    #For example, convert `  -rpcpassword=<pw>` in `rpcpassword`.
    options = []
    for option_entry in help_options:
        cleaned_option = option_entry.strip().split("=")[0]
        cleaned_option = cleaned_option.replace("-", "", 1)
        options.append(cleaned_option)

    return options

def create_datadir():
    """
    Create data directory used by dogecoin daemon.

    Create manually the directory while root at container creation,
    root rights needed to create folder with host volume.
    """
    #Try to get datadir from argv
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-datadir", "--datadir")
    argv, _ = parser.parse_known_args()

    #Try to get datadir from environment
    datadir = argv.datadir or os.environ.get("DATADIR")

    os.makedirs(datadir, exist_ok=True)

    user = os.environ["USER"]
    subprocess.run(["chown", "-R", f"{user}:{user}", datadir], check=True)

def convert_env(executable):
    """
    Convert existing environment variables into command line arguments,
    remove it from the environment.

    Options from executable man pages are searched in the environment,
    converting options in upper case and convert "-" to "_".

    Exemple:
    -rpcuser is RPCUSER
    -help-debug is HELP_DEBUG

    Environment variables can be used with an empty value if the
    corresponding option do not expect a value.
    """
    man_options = executable_options(executable)
    option_to_env = lambda opt_value : opt_value.upper().replace("-", "_")

    cli_arguments = []
    for option in man_options:
        env_option = os.environ.pop(option_to_env(option), None)

        if env_option is not None:
            cli_option = "-" + option
            cli_option += "=" + env_option if env_option else ""
            cli_arguments.append(cli_option)

    return cli_arguments

def run_executable(executable, executable_args):
    """
    Run selected dogecoin executable with arguments from environment and
    command line. Switch manually from root rights needed at startup
    to unprivileged user.

    Manually execve + setuid/setgid to run process as pid 1,
    to manage a single process in a container & more predictive
    signal handling.
    """
    if executable == "dogecoind":
        executable_args.append("-printtoconsole")

    #Switch process from root to user.
    #Equivalent to use gosu or su-exec
    user_info = pwd.getpwnam(os.environ['USER'])
    os.setgid(user_info.pw_gid)
    os.setuid(user_info.pw_uid)

    #Run container command
    return execute(executable, executable_args)

def main():
    """
    Main routine
    """
    if sys.argv[1].startswith("-"):
        executable = "dogecoind"
    else:
        executable = sys.argv.pop(1)

    #Container running arbitrary commands unrelated to dogecoin
    if executable not in CLI_EXECUTABLES:
        return execute(executable, sys.argv[1:])

    create_datadir()

    executable_args = convert_env(executable)
    executable_args += sys.argv[1:]

    return run_executable(executable, executable_args)

if __name__ == "__main__":
    sys.exit(main())
