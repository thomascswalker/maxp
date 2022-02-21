# Standard
import os
import sys
import abc

# Qt
from PySide2.QtWidgets import QMainWindow, QApplication
from PySide2.QtCore import QFile, QSettings, QEvent, QSize
from PySide2.QtUiTools import QUiLoader

# Package
from utils import files


class AutoWindow(QMainWindow):
    _uniqueName: str

    def __init__(
        self,
        title: str,
        parent=None,
        uiFile: str = "",
        unique: bool = True
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        self._uniqueName = self.__class__.__name__
        self.setObjectName(self._uniqueName)
        self._settings = QSettings(self._uniqueName, self._uniqueName)

        if uiFile != "":
            loader = QUiLoader()
            filename = files.relative(f"..\\tools\\{uiFile}.ui")

            if not os.path.exists(filename):
                raise FileNotFoundError(f"File {filename} not found!")

            file = QFile(filename)
            file.open(QFile.ReadOnly)

            self.ui = loader.load(file, self.parent())

            file.close()

            self.setCentralWidget(self.ui)

        if unique:
            self.close_instances()

    def close_instances(self) -> None:
        if self.parentWidget() is None:
            return

        dialogs = self.parentWidget().findChildren(QMainWindow, self._uniqueName)
        for dialog in dialogs:
            if dialog.isVisible():
                dialog.close()

    def read_settings(self) -> None:
        self.move(self._settings.value('pos', QSize(0, 0)))
        self.resize(self._settings.value('size', QSize(640, 480)))

    def write_settings(self) -> None:
        self._settings.setValue('pos', self.pos())
        self._settings.setValue('size', self.size())

    @abc.abstractmethod
    def add_callbacks(self) -> None:
        pass

    @abc.abstractmethod
    def delete_callbacks(self) -> None:
        pass

    # Qt Override
    def showEvent(self, event: QEvent) -> None:
        self.read_settings()
        self.add_callbacks()
        super().showEvent(event)

    # Qt Override
    def closeEvent(self, event: QEvent) -> None:
        self.write_settings()
        self.delete_callbacks()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = AutoWindow()
    dialog.show()
    sys.exit(app.exec_())
