# Standard
import ast
from collections import namedtuple
from typing import Any, List, TypeVar, Union

# 3ds Max
from ..runtime import pymxs, rt


def redraw() -> None:
    rt.redrawViews()


def get_current_selection() -> Union[List, Any]:
    """Get the current selection in the scene.

    - If one object is selected, returns that object.
    - If multiple objects are selected, returns a list of those objects.
    - If no objects are selected, returns None.

    Returns:
        List, Any: The object(s) that is/are selected
    """
    objects = list(rt.GetCurrentSelection())
    if len(objects) == 1:
        return objects[0]
    elif len(objects > 1):
        return objects
    else:
        return None


def get_nodes(selected: bool = False) -> List[NodeInfo]:
    nodes = []
    objects = list(rt.objects)

    if selected:
        objects = list(rt.GetCurrentSelection())

    for node in objects:
        info = NodeInfo(node, node.name, node.material)
        nodes.append(info)

    return nodes


def get_node_by_name(name: str) -> Any:
    return rt.getNodeByName(name)


def is_valid(node: Any) -> bool:
    if node is None:
        return False

    if not rt.isValidNode(node):
        return False

    return True


def has_user_prop(node: Any, prop: str) -> bool:
    if not is_valid(node):
        raise ValueError(f"Node {node} is not valid.")

    value = rt.getUserProp(node, prop)
    return True if value is not None else False


def get_user_prop(node: Any, prop: str) -> Any:
    if not has_user_prop(node, prop):
        raise ValueError(f"Node {node} has no User Property {prop}")

    value = str(rt.getUserProp(node, prop))
    print(f"{prop}={value}")
    return ast.literal_eval(value)


def add_callback(name, method, id):
    rt.callbacks.addScript(rt.name(name), method, id=rt.name(id))


def remove_callback(name, id):
    rt.callbacks.removeScripts(rt.name(name), id=rt.name(id))


def rotate_pivot(obj, rotation):
    tempPosition = obj.position
    inverseRotation = rt.inverse(rt.quat(rotation))
    rt.setRefCoordSys(rt.Name("local"))
    obj.rotation = inverseRotation
    obj.objectoffsetrot = inverseRotation
    obj.objectoffsetpos *= inverseRotation
    obj.position = tempPosition


def export_model(model, filename: str, origin: bool = True, upAxis: str = "Y"):
    rt.select(model)

    if origin:
        tempTransform = model.transform
        model.position = rt.Point3(0, 0, 0)
        model.rotation = rt.Point3(0, 0, 0)
        model.scale = rt.Point3(1, 1, 1)

    # if upAxis == 'Y':
    #     rotation = rt.eulerangles(90,0,0)
    #     rotate_pivot(model, rotation)
    # else:
    #     rotation = rt.eulerangles(0,0,0)
    #     rotate_pivot(model, rotation)

    rt.exportFile(filename, rt.name("noPrompt"), selectedOnly=True, using=rt.FBXEXP)

    if origin:
        model.transform = tempTransform

    rt.redrawViews()
