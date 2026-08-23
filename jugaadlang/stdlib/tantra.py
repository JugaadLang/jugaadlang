"""
tantra — JugaadLang System and Environment Module.
"""

import os
import shlex
import subprocess
import sys

# System attributes
path = sys.path
argv = sys.argv
exit = sys.exit
platform = sys.platform
environment = os.environ

# OS attributes
folder_ka_naam = os.getcwd
badlo_folder = os.chdir
name = os.name
pid = os.getpid


def shell_chalao(command: str) -> int:
    """Run a command and return exit code.

    Uses shlex.split() + shell=False to prevent shell injection.

    On Windows, POSIX-mode splitting would treat backslashes in paths
    like C:\\Users\\... as escape characters, so native mode is used there
    and leftover quote characters are stripped from tokens.
    """
    args = shlex.split(command, posix=os.name != "nt")
    if os.name == "nt":
        args = [arg.strip('"') for arg in args]
    result = subprocess.run(args)  # noqa: S603
    return result.returncode
