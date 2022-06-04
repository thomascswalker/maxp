# noqa
# flake8: noqa
from .util.exceptions import MaxRuntimeError

try:
    import pymxs
    import qtmax
    from pymxs import (MXSWrapperBase, MXSWrapperObjectSet,
                       MXSWrapperObjectSetIter)
    from pymxs import mxsreference as ref
    from pymxs import mxstoken as token
    from pymxs import runtime as rt

    MAX_HWND = qtmax.GetQMaxMainWindow()
except (ImportError, ModuleNotFoundError):
    raise MaxRuntimeError()
