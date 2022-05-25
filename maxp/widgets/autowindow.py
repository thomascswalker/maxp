# Standard
import abc
import os
from typing import Any

# Qt
from PySide2.QtCore import QEvent, QFile, QPoint, QSettings, QSize, Signal, Slot
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSpinBox

# Internal
from .. import maxhwnd, rt
from .. import fileio


def bind(signal: Signal, slot: Slot, node: Any, prop: str) -> rt.NodeEventCallback:
    """Bind a widget to a 3ds Max Node property."""

    def _wexec(value: Any):
        setattr(node, prop, value)

    def _nexec(event, node):
        value = getattr(node, prop)
        slot(value)

    signal.connect(_wexec)
    callback = rt.NodeEventCallback(propertiesOtherEvent=_nexec)
    return callback


def unbind(callback: rt.NodeEventCallback) -> None:
    callback = None


class AutoWindow(QMainWindow):
    """Window with convenience features already setup.

    - Auto-load/save widget properties
    - Load .ui file
    - Kill instances of this window upon launch (ensuring
    only one instance of this window exists)
    """

    _uniqueName: str
    _settings: QSettings

    def __init__(
        self,
        title: str,
        parent: QWidget = maxhwnd,
        uiFile: str = "",
        unique: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        self._uniqueName = self.__class__.__name__
        self.setObjectName(self._uniqueName)
        self._settings = QSettings(self._uniqueName, self._uniqueName)

        if uiFile != "":
            loader = QUiLoader()
            filename = fileio.relative(f"..\\tools\\{uiFile}.ui")

            if not os.path.exists(filename):
                raise FileNotFoundError(f"File {filename} not found!")

            file = QFile(filename)
            file.open(QFile.ReadOnly)

            self.ui = loader.load(file, self.parent())

            file.close()

            self.setCentralWidget(self.ui)

        if unique:
            self.closeInstances()

    # Override
    def showEvent(self, event: QEvent) -> None:
        self.readSettings()
        self.addCallbacks()
        super().showEvent(event)

    # Override
    def closeEvent(self, event: QEvent) -> None:
        self.writeSettings()
        self.deleteCallbacks()
        super().closeEvent(event)

    def closeInstances(self) -> None:
        """Close all instances of this window."""
        if self.parentWidget() is None:
            return

        dialogs = self.parentWidget().findChildren(QMainWindow, self._uniqueName)
        for dialog in dialogs:
            if dialog.isVisible():
                dialog.close()

    def readSettings(self) -> None:
        pos = self._settings.value("pos", QSize(0, 0))  # type: ignore
        self.move(pos)

        size = self._settings.value("size", QSize(640, 480))  # type: ignore
        self.resize(size)

    def writeSettings(self) -> None:
        self._settings.setValue("pos", self.pos())
        self._settings.setValue("size", self.size())

    @abc.abstractmethod
    def addCallbacks(self) -> None:
        pass

    @abc.abstractmethod
    def deleteCallbacks(self) -> None:
        pass


if __name__ == "__main__":

    class TestBindWindow(AutoWindow):
        def __init__(self) -> None:
            super().__init__("Test Bind Window")
            self.setLayout(QVBoxLayout())
            spn = QSpinBox()
            self.layout().addWidget(spn)

            sphere = rt.Sphere()

            bind(spn.valueChanged, spn.setValue, sphere, "radius")

    w = TestBindWindow()
    w.show()
