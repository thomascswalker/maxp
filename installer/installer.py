from glob import glob
import os
import sys
import subprocess
from typing import List, Tuple
from collections import namedtuple

from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2.QtWidgets import QApplication, QMainWindow

GITHUB = r"https://github.com/thomascswalker/better-max-tools"
APPLICATION_PLUGINS_PATH = r"C:\ProgramData\Autodesk\ApplicationPlugins"
AUTODESK_PATH = r"C:\Program Files\Autodesk"
SITE_PACKAGES = os.path.join(os.getenv("appdata"), r"Python\Python37\site-packages")

MaxInstall = namedtuple(
    'MaxInstall',
    [
        'directory',
        'version',
        'pythonExecutable',
        'sitePackages'
    ]
)

def get_max_installs() -> List[Tuple[str]]:

    dirs = glob(AUTODESK_PATH + r"\3ds Max*")
    result = []

    for dir in dirs:
        if os.path.exists(os.path.join(dir, "3dsmax.exe")):
            version = dir.split(" ")[-1]

            if version == 2022:
                pythonExecutable = os.path.join(dir, "Python37\\python.exe")
                sitePackages = os.path.join(os.getenv("appdata"), "Python\\Python37\\site-packages")
            elif version == 2023:
                pythonExecutable = os.path.join(dir, "Python39\\python.exe")
                sitePackages = os.path.join(os.getenv("appdata"), "Python\\Python39\\site-packages")
            else:
                pythonExecutable = os.path.join(dir, "Python\\python.exe")
                sitePackages = os.path.join(os.getenv("appdata"), "Python\\Python37\\site-packages")

            MaxInstall(dir, version, pythonExecutable, sitePackages)
            result.append(MaxInstall)

    return result


def is_package_installed() -> bool:
    return True


class InstallerWindow(QMainWindow):
    _installations: List[MaxInstall] = get_max_installs()
    _currentVersion: str
    _currentMaxPath: str

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Better Max Tools Installer")
        self.setupUi()
        self.setupConnections()
        self.setupStyle()

    def setupUi(self) -> None:
        uiFileName = f"{os.path.dirname(__file__)}\\installer.ui"
        if not os.path.exists(uiFileName):
            raise FileNotFoundError(".ui file not found!")

        loader = QUiLoader()
        file = QFile(uiFileName)
        self._centralWidget = loader.load(file)
        self.setMaximumSize(self._centralWidget.size())

        self.setCentralWidget(self._centralWidget)
        for installation in self._installations:
            print(installation.version)
            print(installation.directory)
            item = (f"3ds Max {installation.version}", installation.directory)
            self._centralWidget.maxVersionList.addItem(*item)
        self._centralWidget.maxVersionList.addItem('test')
        self.setInstallPath()

    def setupConnections(self):
        self._centralWidget.maxVersionExplore.clicked.connect(self.exploreMaxVersion)

        isInstalled = is_package_installed()
        if not isInstalled:
            self._centralWidget.uninstall.setEnabled(False)
            self._centralWidget.install.clicked.connect(self.install)
        else:
            self._centralWidget.install.setEnabled(False)
            self._centralWidget.uninstall.setEnabled(True)
            self._centralWidget.uninstall.clicked.connect(self.uninstall)

    def setupStyle(self):
        qssFileName = f"{os.path.dirname(__file__)}\\windows.qss"
        with open(qssFileName, 'r') as file:
            qss = "".join(file.readlines())
        self.setStyleSheet(qss)

    def setInstallPath(self):
        self._centralWidget.installPath.setText(SITE_PACKAGES)

    def exploreMaxVersion(self):
        path = self._centralWidget.maxVersionList.currentData()
        if os.path.exists(path):
            subprocess.Popen(f'explorer "{path}"')

    def install(self):
        maxPath = self._centralWidget.maxVersionList.currentData()
        version = "37"
        interpreter = os.path.join(maxPath, f"Python{version}\\python.exe")
        if not os.path.exists(interpreter):
            raise FileNotFoundError("Python interpreter not found.")

        subprocess.Popen(f"{interpreter} -m ensurepip")

        packages = ["better-max-tools-thomascswalker"]
        for package in packages:
            subprocess.Popen(f"{interpreter} -m pip install {package}")

    def uninstall(self):
        pass


def run():
    app = QApplication(sys.argv)

    dialog = InstallerWindow()
    dialog.show()

    app.exec_()


if __name__ == "__main__":
    run()
