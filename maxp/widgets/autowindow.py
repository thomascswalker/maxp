# Standard
import abc
import os

# Qt
from PySide2.QtCore import QEvent, QFile, QPoint, QSettings, QSize
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QMainWindow, QWidget

# Internal
from .. import maxhwnd, rt
from ..utils import files


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
            filename = files.relative(rf"..\tools\{uiFile}.ui")

            if not os.path.exists(filename):
                raise FileNotFoundError(f"File {filename} not found!")

            file = QFile(filename)
            file.open(QFile.ReadOnly)

            self.ui = loader.load(file, self.parent())

            file.close()

            self.setCentralWidget(self.ui)

        if unique:
            self.close_instances()

    # Override
    def showEvent(self, event: QEvent) -> None:
        self.read_settings()
        self.add_callbacks()
        super().showEvent(event)

    # Override
    def closeEvent(self, event: QEvent) -> None:
        self.write_settings()
        self.delete_callbacks()
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
        pos = QPoint(self._settings.value("pos", QSize(0, 0)))  # type: ignore
        self.move(pos)

        size = QSize(self._settings.value("size", QSize(640, 480)))  # type: ignore
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
    dialog = AutoWindow("3ds Max Window", parent=maxhwnd)
    dialog.show()
