# This is to easily import functions/ files from elsewhere in the project directly into testing files that are using
# pytest

import sys
import os

# so that python knows to look inside root/backend to find "app"
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))
