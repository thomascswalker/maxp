from .exceptions import MaxRuntimeError

try:
    import qtmax
    import pymxs
    from pymxs import runtime as rt
    from pymxs import mxsreference as ref
    from pymxs import mxstoken as token
    from pymxs import MXSWrapperBase, MXSWrapperObjectSet, MXSWrapperObjectSetIter

    MAX_HWND = qtmax.GetQMaxMainWindow()
except (ImportError, ModuleNotFoundError):
    raise MaxRuntimeError()
