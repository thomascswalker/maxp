# Standard
import inspect
import os
from typing import List

# Package
from maxp import rt
from maxp.util import scene
from maxp.util.exceptions import InvalidNodeError


def relative(filename: str) -> str:
    """Find a file from a relative file path and name. Uses '..' to define leaves.

    Usage::
    ```
    relative('..\\\\..\\\\test.txt')
    ```

    Args:
        filename (str): The relative filename, as well as any leaves to go up.

    Returns:
        str: The constructed filename.
    """
    leaves = filename.split("\\")
    count = leaves.count("..") + 1

    calledFrom = inspect.stack()[1].filename
    commonLeaves = calledFrom.split("\\")
    commonRoot = "\\".join(commonLeaves[: (len(commonLeaves) - count)])

    end = [leaf for leaf in leaves if leaf != ".."]
    return os.path.join(commonRoot, "\\".join(end))


def mergeFile(filename: str) -> None:
    if not os.path.exists(filename):
        raise FileNotFoundError(f"{filename} not found!")

    rt.MergeMaxFile(filename)


def mergeFiles(filenames: List[str]) -> None:
    for filename in filenames:
        mergeFile(filename)


def loadFile(filename: str) -> None:
    if not os.path.exists(filename):
        raise FileNotFoundError(f"{filename} not found!")

    rt.LoadMaxFile(filename)


def importFile(filename: str) -> None:
    if not os.path.exists(filename):
        raise FileNotFoundError(f"{filename} not found!")

    rt.ImportFile(filename)


def importFiles(filenames: List[str]) -> None:
    for filename in filenames:
        importFile(filename)


def exportNode(node: rt.Node, filepath: str, fileext: str) -> str:
    if not scene.isValid(node):
        raise InvalidNodeError(node)
    rt.Select(node)
    if fileext == ".fbx":
        exporter = rt.FBXEXP
    elif fileext == ".obj":
        exporter = rt.ObjExp
    else:
        raise ValueError(f"Invalid export file format, got {fileext}")
    filename = os.path.join(filepath, f"{node.name}.{fileext}")
    rt.ExportFile(filename, rt.Name("noPrompt"), selectedOnly=True, using=exporter)

    return filename


def exportNodes(nodes: List[rt.Node], filepath: str, fileext: str) -> List[str]:
    filenames = []

    for node in nodes:
        filename = exportNode(node, filepath, fileext)
        filenames.append(filename)

    return filenames
