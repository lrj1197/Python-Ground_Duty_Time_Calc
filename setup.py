# """
# This is a setup.py script generated by py2applet
#
# Usage:
#     python setup.py py2app
# """
#
# from setuptools import setup
#
# APP = ['main_win.py']
# DATA_FILES = [""]
# OPTIONS = {}
#
# setup(
#     app=APP,
#     data_files=DATA_FILES,
#     options={'py2app': OPTIONS},
#     setup_requires=['py2app'],
# )




import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

build_options = {"build_exe": build_exe_options, "build_dmg":}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"
# elif sys.platform == "osx":
#     base = "OSX"

setup(  name = "guifoo",
        version = "0.1",
        description = "My GUI application!",
        options = build_options,
        executables = [Executable("main_win.py", base=base)])