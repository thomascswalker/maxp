# Standard
import os
from typing import Optional

# Qt
from PySide2.QtCore import QEvent
from PySide2.QtWidgets import QFileDialog

# Package
from utils import maxscript
from widgets.autowindow import AutoWindow


class GameExporterWindow(AutoWindow):
    _modelQueue = []

    def __init__(self, parent=None):
        super().__init__(parent=parent, title='Game Exporter', uiFile='gameexporter')
        self.setup_connections()
        self.populate_models_list()

    def setup_connections(self):
        self.ui.exportSelected.toggled.connect(self.on_export_selected_checked)
        self.ui.exploreOutput.clicked.connect(self.on_explore_output_clicked)
        self.ui.exportModels.clicked.connect(self.export_models)

    def add_callbacks(self):
        maxscript.add_callback('selectionSetChanged', self.populate_models_list, 'GameExporter')

    def delete_callbacks(self):
        maxscript.remove_callback('selectionSetChanged', 'GameExporter')

    def on_explore_output_clicked(self):
        output = QFileDialog.getExistingDirectory(self, "Select output directory")
        self.ui.filePath.setText(output)

    def on_export_selected_checked(self, state: bool) -> None:
        self.populate_models_list()

    def populate_models_list(self) -> None:
        self.ui.modelList.clear()
        self._modelQueue = []

        nodes = maxscript.get_nodes(selected=self.ui.exportSelected.isChecked())
        for node in nodes:
            self.ui.modelList.addItem(node.name)
            self._modelQueue.append(node)

    def get_up_axis(self):
        upAxis = self.ui.upAxis.currentIndex()

        if upAxis == 0:
            return "Y"

        return "Z"

    def export_models(self):
        upAxis = self.get_up_axis()
        origin = self.ui.moveToOrigin.isChecked()
        path = self.ui.filePath.text()
        prefix = self.ui.filePrefix.text()

        for model in self._modelQueue:
            obj = model.reference
            name = model.name
            filename = os.path.join(path, prefix + name + ".fbx")
            maxscript.export_model(obj, filename, origin=origin, upAxis=upAxis)

    # Qt Override
    def showEvent(self, event: QEvent) -> None:
        self.add_callbacks()
        self.read_settings()
        super().showEvent(event)

    # Qt Override
    def closeEvent(self, event: QEvent) -> None:
        self.delete_callbacks()
        self.write_settings()
        super().closeEvent(event)
