# Standard
from typing import List

# Qt
from PySide2.QtWidgets import QFileDialog
from maxp import fileio

# Package
from maxp.widgets.autowindow import AutoWindow
from maxp import callbacks, scene
from maxp.callbacks import GeneralEvent


class GameExporterWindow(AutoWindow):
    _modelQueue: List = []

    def __init__(self, parent=None):
        super().__init__("Game Exporter", parent=parent, uiFile="gameexporter")
        self.setup_connections()
        self.populate_models_list()

    def setup_connections(self) -> None:
        self.ui.exportSelected.toggled.connect(self.on_export_selected_checked)
        self.ui.exploreOutput.clicked.connect(self.on_explore_output_clicked)
        self.ui.exportModels.clicked.connect(self.export_models)

    def add_callbacks(self) -> None:
        super().add_callbacks()
        callbacks.add(
            GeneralEvent.selectionSetChanged,
            self.populate_models_list,
            id="GameExporter",
        )

    def delete_callbacks(self) -> None:
        super().delete_callbacks()
        callbacks.remove(
            GeneralEvent.selectionSetChanged,
            id="GameExporter",
        )

    def on_explore_output_clicked(self):
        output = QFileDialog.getExistingDirectory(self, "Select output directory")
        self.ui.filePath.setText(output)

    def on_export_selected_checked(self, state: bool) -> None:
        self.populate_models_list()

    def populate_models_list(self) -> None:
        self.ui.modelList.clear()
        self._modelQueue = []

        nodes = scene.getNodes(selected=self.ui.exportSelected.isChecked())
        for node in nodes:
            self.ui.modelList.addItem(node.name)
            self._modelQueue.append(node)

    def get_up_axis(self):
        upAxis = self.ui.upAxis.currentIndex()

        if upAxis == 0:
            return "Y"

        return "Z"

    def export_models(self):
        # upAxis = self.get_up_axis()
        # origin = self.ui.moveToOrigin.isChecked()
        path = self.ui.filePath.text()
        # prefix = self.ui.filePrefix.text()

        for model in self._modelQueue:
            fileio.exportNode(model, path, ".fbx")


if __name__ == "__main__":
    w = GameExporterWindow()
    w.show()
