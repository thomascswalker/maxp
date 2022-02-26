from modulefinder import Module


try:
    from pymxs import runtime as rt
    import qtmax
    maxhwnd = qtmax.GetQMaxMainWindow()
except (ImportError, ModuleNotFoundError):
    rt = None
    maxhwnd = None
