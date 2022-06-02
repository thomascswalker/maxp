import os
from ..maxp import rt, nodes, fileio, context


def test_originExport():
    sphere = rt.Sphere()
    origPos = rt.Point3(25, 5, 50)
    nodes.setProperty(sphere, "transform.position", origPos)
    path = "C:\\Users\\Tom\\Desktop"
    ext = ".obj"
    with context.origin(sphere):
        filename = fileio.exportNode(sphere, path, ext)

    assert sphere.transform.position == origPos
    assert os.path.exists(filename)