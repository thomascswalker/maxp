from glob import glob
import os
import sys
import subprocess
from typing import List, Tuple
from collections import namedtuple

from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2.QtWidgets import QApplication, QMainWindow, QMessageBox

PACKAGE = "better-max-tools-thomascswalker"
GITHUB = r"https://github.com/thomascswalker/better-max-tools"
APPLICATION_PLUGINS_PATH = r"C:\ProgramData\Autodesk\ApplicationPlugins"
AUTODESK_PATH = r"C:\Program Files\Autodesk"
SITE_PACKAGES = os.path.join(os.getenv("appdata"), r"Python\Python37\site-packages")

MaxInstall = namedtuple(
    "MaxInstall", ["directory", "version", "pythonExecutable", "sitePackages"]
)


def get_max_installs() -> List[Tuple[str]]:
    dirs = glob(AUTODESK_PATH + r"\3ds Max*")
    result = []

    for dir in dirs:
        if os.path.exists(os.path.join(dir, "3dsmax.exe")):
            version = dir.split(" ")[-1]

            if version == 2022:
                pythonExecutable = os.path.join(dir, "Python37\\python.exe")
                sitePackages = os.path.join(
                    os.getenv("appdata"), "Python\\Python37\\site-packages"
                )
            elif version == 2023:
                pythonExecutable = os.path.join(dir, "Python39\\python.exe")
                sitePackages = os.path.join(
                    os.getenv("appdata"), "Python\\Python39\\site-packages"
                )
            else:
                pythonExecutable = os.path.join(dir, "Python37\\python.exe")
                sitePackages = os.path.join(
                    os.getenv("appdata"), "Python\\Python37\\site-packages"
                )

            install = MaxInstall(dir, version, pythonExecutable, sitePackages)
            result.append(install)

    return result


def is_package_installed(install: MaxInstall) -> bool:
    args = [install.pythonExecutable, "-m", "pip", "list"]
    result = subprocess.check_output(args)
    for line in result.decode().split("\n"):
        if "better-max-tools" in line:
            return True

    return False


def install_package(install: MaxInstall) -> bool:
    interpreter = install.pythonExecutable
    if not os.path.exists(interpreter):
        raise FileNotFoundError("Python interpreter not found.")

    subprocess.Popen(f"{interpreter} -m ensurepip")

    args = [interpreter, "-m", "pip", "install", PACKAGE]
    output = subprocess.check_output(args)

    QMessageBox.information(None, "Better Max Tools", "Installed!")

    return True


def uninstall_package(install: MaxInstall) -> bool:
    interpreter = install.pythonExecutable
    if not os.path.exists(interpreter):
        raise FileNotFoundError("Python interpreter not found.")

    subprocess.Popen(f"{interpreter} -m ensurepip")

    args = [interpreter, "-m", "pip", "uninstall", "-y", PACKAGE]
    output = subprocess.check_output(args)

    QMessageBox.information(None, "Better Max Tools", "Uninstalled!")

    return True


class InstallerWindow(QMainWindow):
    _installations: List[MaxInstall] = get_max_installs()
    _currentInstall: MaxInstall = _installations[0]

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Better Max Tools Installer")
        self.setupUi()
        self.setupConnections()
        self.updateInstallButtonState()
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
            item = (f"3ds Max {installation.version}", installation.directory)
            self._centralWidget.maxVersionList.addItem(*item)

        self.setInstallPath()

    def setupConnections(self):
        self._centralWidget.maxVersionExplore.clicked.connect(self.exploreMaxVersion)
        self._centralWidget.install.clicked.connect(self.install)
        self._centralWidget.uninstall.clicked.connect(self.uninstall)

    def updateInstallButtonState(self):
        isInstalled = is_package_installed(self._currentInstall)
        if not isInstalled:
            self._centralWidget.install.setEnabled(True)
            self._centralWidget.uninstall.setEnabled(False)
        else:
            self._centralWidget.install.setEnabled(False)
            self._centralWidget.uninstall.setEnabled(True)

    def setupStyle(self):
        qssFileName = f"{os.path.dirname(__file__)}\\windows.qss"
        with open(qssFileName, "r") as file:
            qss = "".join(file.readlines())
        self.setStyleSheet(qss)

    def setInstallPath(self):
        self._centralWidget.installPath.setText(SITE_PACKAGES)

    def exploreMaxVersion(self):
        path = self._centralWidget.maxVersionList.currentData()
        if os.path.exists(path):
            subprocess.Popen(f'explorer "{path}"')

    def install(self):
        install_package(self._currentInstall)
        self.updateInstallButtonState()

    def uninstall(self):
        uninstall_package(self._currentInstall)
        self.updateInstallButtonState()


def main():
    app = QApplication(sys.argv)

    dialog = InstallerWindow()
    dialog.show()

    app.exec_()


if __name__ == "__main__":
    main()
