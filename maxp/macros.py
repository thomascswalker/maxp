# Standard
from collections import namedtuple
import re
from typing import Callable, List

# Package
from maxp import rt
from maxp.tools import gameexporter

# Defines a wrapper for MacroScript properties
Macro = namedtuple(
    "Macro",
    [
        "id",
        "action",
        "category",
        "internalCategory",
        "sourceFileName",
        "macroBtnIcon",
        "btnIconIndex",
    ],
)


def getMacros() -> List[Macro]:
    """Return all macros in the current 3ds Max session."""
    macros = []
    stream = rt.StringStream("")
    rt.Macros.list(to=stream)
    lines = str(stream).splitlines()
    for line in lines:
        fields = re.findall("([\"'])(?:(?=(\\?))\2.)*?\1|[0-9]", line)
        macros.append(Macro(*fields))
    return macros


def isMacroDefined(action: str, category: str) -> bool:
    """Return if the given action (in category) exists as a macro."""
    return any([m.action == action and m.category == category for m in getMacros()])


def addMacro(
    action: str, category: str, title: str, tooltip: str, func: Callable
) -> None:
    """Add a new macro to 3ds Max.

    Args:
        action (str): The name of the macro.
        category (str): The category the macro can be found in.
        title (str): The button text or menu entry name.
        tooltip (str): Text displayed when hovered.
        func (Callable): The method to execute when calling the macro.
    """
    mxs = f"""
    from {func.__module__} import {func.__name__}
    {func}()
    """
    rt.Macros.new(category, action, tooltip, title, mxs)


def test_addMacro():
    addMacro(
        "GameExporter",
        gameexporter.__package__,
        "Game Exporter",
        gameexporter.__doc__,
        gameexporter.launch,
    )
    assert isMacroDefined("GameExporter", "maxp")
