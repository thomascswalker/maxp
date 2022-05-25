# Standard
import math

# maxp
from .. import rt
from ..utils import maxscript


def createCamera() -> rt.Camera:
    camera = rt.targetCamera(target=rt.targetObject())
    camera.fov = 25.0
    return camera


def alignCamera(camera: rt.Camera, object: rt.Node):
    # Move the target position to the center of the target object
    target = camera.target
    target.pos = object.center
    fov = camera.fov

    # Get the bounds of the object
    bounds = object.max - object.min

    # Get the largest bounding box dimension
    radius = max([bounds.x, bounds.y, bounds.z])

    # Calculate the distance to fit into the view, given
    # the FOV and radius
    dist = (radius / 2.0) / math.tan(math.radians(fov) / 2.0)

    # Construct the goal position
    goalPos = rt.Point3(dist, dist, dist)

    # Move the camera and set the FOV
    camera.pos = goalPos


def createIconCamera(obj: rt.Node):
    camera = createCamera()
    alignCamera(camera, obj)
    rt.viewport.setCamera(camera)


def setViewport(camera: rt.Camera) -> None:
    rt.viewport.setCamera(camera)


if __name__ == "__main__":
    obj = maxscript.get_current_selection()
    createIconCamera(obj)
