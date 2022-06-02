from typing import Any


class MaxRuntimeError(Exception):
    def __init__(self) -> None:
        msg = "Module pymxs not found. Are you running this script in 3ds Max?"
        super().__init__(msg)


class InvalidNodeError(Exception):
    def __init__(self, node: Any) -> None:
        msg = f"Node {node} is not valid."
        super().__init__(msg)


class DeletedNodeError(Exception):
    def __init__(self, node: Any) -> None:
        msg = f"Node {node} is deleted."
        super().__init__(msg)
