# Python Modules
import atexit

# Maya Modules
import maya.standalone as standalone

standalone.initialize(name="python")
atexit.register(standalone.uninitialize)

