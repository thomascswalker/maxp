from maxp import callbacks, nodes, rt
from maxp.callbacks import GeneralEvent


def test_addCallback() -> bool:
    callbacks.remove(GeneralEvent.nodeCreated)

    def func(*args):
        obj = rt.callbacks.notificationParam()
        nodes.setProperty(obj, "radius", 5.0)

    callbacks.add(GeneralEvent.nodeCreated, func)

    obj = rt.Sphere()
    radius = nodes.getProperty(obj, "radius")

    callbacks.remove(GeneralEvent.nodeCreated)

    assert radius == 5.0, f"radius == {radius}"

    return True


def test_removeCallback() -> bool:
    def func(*args):
        obj = rt.callbacks.notificationParam()
        nodes.setProperty(obj, "pos.x", 5.0)

    callbacks.remove(GeneralEvent.nodeCreated)

    obj = rt.Sphere()
    radius = nodes.getProperty(obj, "radius")
    assert radius == 25.0, f"radius == {radius}"

    return True


if __name__ == "__main__":
    test_addCallback()
    test_removeCallback()
