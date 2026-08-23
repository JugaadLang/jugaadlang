"""
tantra — JugaadLang System and Environment Module.
"""

import sys
import os
import shlex
import subprocess

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
    """
    args = shlex.split(command)
    result = subprocess.run(args)  # noqa: S603
    return result.returncode
