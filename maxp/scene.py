"""
Node operations. These are generally wrappers for the MAXScript equivalent,
but handle Python typing.
"""

# Standard
from cmath import isclose
from typing import Any, List, Union

# Internal
from maxp import MXSWrapperBase, rt


def isValid(node: rt.Node) -> bool:
    """Wrapper for MAXScript IsValidNode.

    Return True if `node` is a node value, and the node has not been deleted.
    Otherwise, return False."""
    return rt.IsValidNode(node)


def isClass(node: rt.Node, type: Union[str, Any]) -> bool:
    """Wrapper for MAXScript classOf.

    Returns the value's class. Each type of value has its own class. If the value is a
    Node value, classOf() returns the class of the world state object (the state of the
    node at the top of its stack).
    """
    if not isinstance(node, MXSWrapperBase):
        msg = f"{node} is not a MAXScript object. Try using isinstance instead?"
        raise TypeError(msg)

    if not isValid(node):
        raise ValueError(f"{node} is not valid.")

    if isinstance(type, str):
        type = rt.Execute(type)

    return rt.ClassOf(node, type)


def isSubClass(node: rt.Node, type: Union[str, Any]) -> bool:
    """Wrapper for MAXScript isKindOf.

    Return True if value has given class or inherits from class.
    """
    if not isinstance(node, MXSWrapperBase):
        msg = f"{node} is not a MAXScript object. Try using isinstance instead?"
        raise TypeError(msg)

    if not isValid(node):
        raise ValueError(f"{node} is not valid.")

    if isinstance(type, str):
        type = rt.Execute(type)

    return rt.IsKindOf(node, type)


def getNodeByName(name: str) -> rt.Node:
    """Wrapper for MAXScript getNodeByName.

    Return the first node with the specified name.
    """
    return rt.getNodeByName(name)


def getNodesByName(names: List[str]) -> List[rt.Node]:
    """Return all nodes found with the specified list of names."""
    nodes = []
    for name in names:
        node = getNodeByName(name)
        if node is None:
            continue
        nodes.append(node)
    return nodes


def getNodes(type: Any = None, selected: bool = False) -> List[rt.Node]:
    """Return all nodes in the scene. Optionally, if `type` is specified, return
    only nodes of the specified type.
    """
    if selected:
        nodes = rt.GetCurrentSelection()
    else:
        nodes = [node for node in rt.Objects if isValid(node)]
    if not type:
        nodes = [node for node in nodes if isClass(node, type)]
    return nodes


def getSelected() -> List[rt.Node]:
    """Return the current selection as a list."""
    return rt.GetCurrentSelection()


def hasProperty(node: rt.Node, name: str) -> bool:
    """Return True if `node` has the property `name`. Otherwise, return False."""
    if isinstance(node, MXSWrapperBase):
        try:
            node.getmxsprop(name)
            return True
        except AttributeError:
            return False
    else:
        return hasattr(node, name)


def getProperty(node: rt.Node, name: str) -> Any:
    """Return value from `node` property `name`."""
    if not hasProperty(node, name):
        raise AttributeError(f"{node} has no property {name}")
    if isinstance(node, MXSWrapperBase):
        return node.getmxsprop(name)
    else:
        return getattr(node, name)


def setProperty(node: rt.Node, name: str, value: Any) -> None:
    """Set value on `node` property `name`.

    Handles setting nested values within a node. This sets (and compares) the actual
    value on the node, as opposed to, in some cases, the object generated from setting
    the value.

    For example::
    ```python
    b = rt.Box()
    b.pos.x = 5
    print(b.pos.x) # This will print 0
    ```

    Setting the property directly with setProperty::
    ```python
    b = rt.Box()
    setProperty(b, 'pos.x', 5)
    print(b.pos.x) # This will now print 5
    ```

    See Accessing Object Properties and Controllers on 3ds Max Python docs
    for more details.
    """
    if not hasProperty(node, name):
        raise AttributeError(f"{node} has no property {name}")
    if isinstance(node, MXSWrapperBase):
        node.setmxsprop(name, value)
    else:
        setattr(node, name, value)
    if isinstance(value, float):
        assert isclose(getProperty(node, name), (value), rel_tol=0.001)
    else:
        assert getProperty(node, name) == value
