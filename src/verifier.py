# coding: utf-8
# Verify existence of required libraries in order to run the game properly
# Created by James Raphael Tiovalen (2020)

import sys
import subprocess
import pkg_resources


def check():
    if sys.platform == "win32":
        required = {'libdw', 'windows-curses'}
    else:
        required = {'libdw', 'curses'}

    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed

    if missing:
        try:
            python = sys.executable
            subprocess.check_call(
                [python, '-m', 'pip', 'install', *missing])

        except Exception as e:
            print(e)
            return False
    
    return True
