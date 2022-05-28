from typing import Union, Callable, List

from pymxs import runtime as rt


class Attributes:
    Topology = "topology"
    Geometry = "geometry"
    Names = "names"
    Transform = "transform"
    Select = "select"
    Parameters = "parameters"
    SubAnimStructure = "subAnimStructure"
    Controller = "controller"
    Children = "children"


class Trigger:
    Changes: str = "changes"
    Deleted: str = "deleted"


class HandleMode:
    RedrawViews: rt.Name = rt.Name("redrawViews")
    TimeChange: rt.Name = rt.Name("timeChange")


class When:
    _attr: Attributes
    _objs: Union[rt.Node, List[rt.Node]]
    _trigger: Trigger

    def __init__(
        self,
        attr: Attributes,
        objs: Union[rt.Node, List[rt.Node]],
        trigger: Trigger,
        method: Callable,
    ):
        self._attr = attr
        self._objs = [objs] if not isinstance(objs, list) else objs
        self._trigger = trigger
        self._method = method
        self._exec()

    def _exec(self):
        rt._tempMethod = None
        rt._tempMethod = self._method
        mxsArray = "#(" + ",".join(["$" + obj.name for obj in self._objs]) + ")"
        mxs = f"""
        when {self._attr} {mxsArray} {self._trigger} node do (
            _tempMethod node
        )
        """
        rt.Execute(mxs)


def printer(obj):
    print(obj.radius)


def testWhen():
    sphere = rt.Sphere()
    When(Attributes.Parameters, sphere, Trigger.Changes, printer)


testWhen()
