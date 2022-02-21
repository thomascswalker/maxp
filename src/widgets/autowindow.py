# Standard
import os
import sys

# Qt
from PySide2.QtWidgets import QMainWindow, QApplication
from PySide2.QtCore import QFile, QSettings
from PySide2.QtUiTools import QUiLoader

# Package
from utils import files


class AutoWindow(QMainWindow):
    def __init__(
        self,
        parent=None,
        title: str = "Auto Window",
        uiFile: str = ""
    ) -> None:
        super().__init__(parent)
        className = str(self.__class__)
        self._settings = QSettings(className, className)
        self.setWindowTitle(title)

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

    def read_settings(self) -> None:
        if self._settings is None:
            return

    def write_settings(self) -> None:
        if self._settings is None:
            return

    # Override
    def showEvent(self, event):
        self.read_settings()
        super().showEvent(event)

    # Override
    def closeEvent(self, event):
        self.write_settings()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = AutoWindow()
    dialog.show()
    sys.exit(app.exec_())
