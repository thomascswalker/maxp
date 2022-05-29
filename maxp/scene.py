from cmath import isclose
from typing import Any, List, Union
from . import rt


def isValid(node: rt.Node) -> bool:
    return rt.IsValidNode(node)


def isClass(node: rt.Node, type: Union[str, Any]) -> bool:
    if not isValid(node):
        raise ValueError(f"{node} is not valid.")

    if isinstance(type, str):
        type = rt.Execute(type)

    return rt.ClassOf(node, type)


def isSubClass(node: rt.Node, type: Union[str, Any]) -> bool:
    if not isValid(node):
        raise ValueError(f"{node} is not valid.")

    if isinstance(type, str):
        type = rt.Execute(type)

    return rt.IsKindOf(node, type)


def getNodeByName(name: str) -> rt.Node:
    return rt.Execute(f"${name}")


def getNodes(type: Any = None) -> List[rt.Node]:
    nodes = [node for node in rt.Objects if isValid(node)]
    if not type:
        nodes = [node for node in nodes if isClass(node, type)]
    return nodes


def getSelected() -> List[rt.Node]:
    return rt.GetCurrentSelection()


def hasProperty(node: rt.Node, name: str) -> bool:
    return hasattr(node, name)


def getProperty(node: rt.Node, name: str) -> Any:
    if not hasProperty(node, name):
        raise AttributeError(f"{node} has no property {name}")
    return getattr(node, name)


def setProperty(node: rt.Node, name: str, value: Any) -> None:
    if not hasProperty(node, name):
        raise AttributeError(f"{node} has no property {name}")
    setattr(node, name, value)
    if isinstance(value, float):
        assert isclose(getProperty(node, name), (value), rel_tol=0.001)
    else:
        assert getProperty(node, name) == value
