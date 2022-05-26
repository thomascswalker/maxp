from maxp import rt
from maxp.widgets import autowindow

from PySide2.QtWidgets import QSpinBox, QVBoxLayout

import importlib

importlib.reload(autowindow)


class TestBindWindow(autowindow.AutoWindow):
    def __init__(self) -> None:
        super().__init__("Test Bind Window")
        self.ui.setLayout(QVBoxLayout())
        spn = QSpinBox()
        self.ui.layout().addWidget(spn)

        sphere = rt.Sphere()
        autowindow.bind(spn.valueChanged, spn.setValue, sphere, "radius")


w = TestBindWindow()
w.show()
