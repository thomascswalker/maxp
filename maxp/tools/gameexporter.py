"""
Game exporter similar to the built-in 3ds Max one. This window has more controls
and options for batch exporting and performing certain operations while exporting.
"""

# Standard
import logging
from typing import List

# Qt
from PySide2.QtWidgets import QFileDialog

# Package
from maxp import MAX_HWND, pymxs, rt
from maxp.util import callbacks, fileio, macros, scene
from maxp.util.callbacks import GeneralEvent
from maxp.util.context import origin
from maxp.util.logger import log
from maxp.widgets.autowindow import AutoWindow


class GameExporter(AutoWindow):
    _modelQueue: List[rt.Node] = []

    def __init__(self):
        super().__init__("Game Exporter", parent=MAX_HWND, uiFileName="gameexporter")
        self.setupConnections()
        self.updateModelQueue()

    def setupConnections(self) -> None:
        log("Setting connections")
        self.ui.exportSelected.toggled.connect(self.updateModelQueue)
        self.ui.exploreOutput.clicked.connect(self.exploreOutput)
        self.ui.exportModels.clicked.connect(self.exportQueue)

    def addCallbacks(self) -> None:
        log("Adding callbacks")
        super().addCallbacks()
        callbacks.add(
            GeneralEvent.selectionSetChanged,
            self.updateModelQueue,
            id="GameExporter",
        )

    def removeCallbacks(self) -> None:
        log("Removing callbacks")
        super().removeCallbacks()
        callbacks.remove(
            GeneralEvent.selectionSetChanged,
            id="GameExporter",
        )

    def exploreOutput(self):
        log("Exploring output")
        output = QFileDialog.getExistingDirectory(self, "Select output directory")
        if output != "":
            log(f"Setting output path to {output}")
            self.ui.filePath.setText(output)
        else:
            log(f"No output selected", level=logging.WARNING)

    def updateModelQueue(self) -> None:
        self.clearQueue()
        log(f"Updating model queue")
        selected = self.ui.exportSelected.isChecked()
        nodes = scene.getNodes(selected=selected)
        for node in nodes:
            log(f"Adding model {node.name}", indentLevel=1)
            self.ui.modelList.addItem(node.name)
            self._modelQueue.append(node)

    def clearQueue(self) -> None:
        log(f"Clearing model queue")
        self._modelQueue = []
        self.ui.modelList.clear()

    def exportQueue(self):
        path = self.ui.filePath.text()
        log(f"Exporting model queue at {path}")
        for node in self._modelQueue:
            with origin(node):
                log(f"Moving model {node.name} to origin", indent=1)
                with pymxs.redraw(False):
                    log(f"Disabling redraw", indent=1)
                    log(f"Exporting model {node.name}", indent=1)
                    filename = fileio.exportNode(node, path, ".fbx")
                    log(f"Output model to {filename}", indent=1)


def launch() -> None:
    w = GameExporter()
    w.show()


def test_addMacro():
    macros.addMacro(
        "GameExporter",
        __file__.__package__,
        "Game Exporter",
        __file__.__doc__,
        launch,
    )
    assert macros.isMacroDefined("GameExporter", "maxp")


if __name__ == "__main__":
    launch()
