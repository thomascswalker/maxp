from .runtime import rt


def toArray(iterable: list) -> rt.Array:
    mxsArray = rt.Array()
    for item in iterable:
        rt.Append(mxsArray, item)
    return mxsArray
