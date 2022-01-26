# :coding: utf-8

# Python Modules
import os
import sys

# Platforms
PLATFORM = sys.platform
WINDOWS = "win32"
OSX = "darwin"
LINUX = "linux"


# Paths
GLOBALS_PATH = os.path.abspath(__file__)
SCRIPTS_PATH = os.path.dirname(os.path.dirname(os.path.dirname(GLOBALS_PATH)))
PROJECT_PATH = os.path.dirname(SCRIPTS_PATH)
PLUGINS_PATH = os.path.join(PROJECT_PATH, "plug-ins")
LIB_PATH = os.path.join(PROJECT_PATH, "lib")
LIB_WINDOWS64_PATH = os.path.join(LIB_PATH, "win64")
LIB_OSX_PATH = os.path.join(LIB_PATH, "osx")
LIB_LINUX_PATH = os.path.join(LIB_PATH, "linux")
BIN_PATH = os.path.join(PROJECT_PATH, "bin")
BIN_WINDOWS64_PATH = os.path.join(BIN_PATH, "win64")
BIN_OSX_PATH = os.path.join(BIN_PATH, "osx")
BIN_LINUX_PATH = os.path.join(BIN_PATH, "linux")
DOCS_PATH = os.path.join(PROJECT_PATH, "docs")
USER_PATH = os.path.expanduser('~')
DATA_PATH = os.path.join(SCRIPTS_PATH, "data")

# User

# Maya
MAYA_WINDOW_NAME = "MayaWindow"

if __name__ == "__main__":
    print(GLOBALS_PATH)
    print(DATA_PATH)


