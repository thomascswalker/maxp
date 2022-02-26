# Standard
from typing import List
from collections import namedtuple

# 3ds Max
from bettermaxtools import rt

NodeInfo = namedtuple("NodeInfo", ["reference", "name", "material"])


def get_nodes(selected: bool = False) -> List[NodeInfo]:
    nodes = []
    objects = list(rt.objects)

    if selected:
        objects = list(rt.GetCurrentSelection())

    for node in objects:
        info = NodeInfo(node, node.name, node.material)
        nodes.append(info)

    return nodes


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
