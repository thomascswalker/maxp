from glob import glob
import os
import sys
import subprocess
from typing import List, Tuple
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLineEdit,
    QLabel,
    QToolButton,
    QHBoxLayout,
    QVBoxLayout,
    QFormLayout,
    QFrame,
    QComboBox,
    QWidget,
)

GITHUB = r"https://github.com/thomascswalker/better-max-tools"
APPLICATION_PLUGINS_PATH = r"C:\ProgramData\Autodesk\ApplicationPlugins"
AUTODESK_PATH = r"C:\Program Files\Autodesk"
SITE_PACKAGES = os.path.join(os.getenv("appdata"), "Python\Python37\site-packages")


def get_max_installs() -> List[Tuple[str]]:
    dirs = glob(AUTODESK_PATH + r"\3ds Max*")
    result = []
    for dir in dirs:
        if os.path.exists(os.path.join(dir, "3dsmax.exe")):
            version = dir.split(" ")[-1]
            result.append((dir, version))
    return result


class InstallerWindow(QMainWindow):
    _currentVersion: str
    _currentMaxPath: str

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Better Max Tools Installer")
        self.setupUi()

    def setupUi(self) -> None:
        centralWidget = QFrame()
        layout = QHBoxLayout()

        self._maxVersionList = QComboBox()
        for version in get_max_installs():
            self._maxVersionList.addItem(version[1], version[0])
        self._maxVersionPath = QLineEdit()

        self._maxVersionExplore = QToolButton()
        self._maxVersionExplore.setText("Explore..")
        self._maxVersionExplore.clicked.connect(self.install)

        layout.addWidget(self._maxVersionList)
        layout.addWidget(self._maxVersionExplore)

        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def exploreMaxVersion(self):
        path = self._maxVersionList.currentData()
        if os.path.exists(path):
            subprocess.Popen(f'explorer "{path}"')

    def install(self):
        maxPath = self._maxVersionList.currentData()
        interpreter = os.path.join(maxPath, r"Python37\python.exe")
        if not os.path.exists(interpreter):
            raise FileNotFoundError("Python interpreter not found.")

        subprocess.Popen(f"{interpreter} -m ensurepip")
        subprocess.Popen(f"{interpreter} -m pip install {GITHUB}")


def run():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    dialog = InstallerWindow()
    dialog.show()

    app.exec_()


if __name__ == "__main__":
    run()
