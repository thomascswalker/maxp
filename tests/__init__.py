import os
import sys

MAXP_PATH = os.path.dirname(os.path.dirname(__file__))
if MAXP_PATH not in sys.path:
    sys.path.append(MAXP_PATH)
