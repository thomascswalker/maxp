# Standard
import abc
import os
from typing import Any, Callable, List

# Qt
from PySide2.QtCore import QEvent, QFile, QSettings, QSize, Signal
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QMainWindow, QWidget

# Internal
from .. import maxhwnd, rt
from .. import fileio


class Binding:
    """Bind a QWidget object to a 3ds Max node property and vice versa."""

    _signal: Signal
    _slot: Callable[[Any], None]
    _node: rt.Node
    _prop: str
    _callback: rt.NodeEventCallback

    def __init__(
        self, signal: Signal, slot: Callable[[Any], None], node: rt.Node, prop: str
    ) -> None:
        self._signal = signal
        self._slot = slot  # type: ignore
        self._node = node
        self._prop = prop

        self._signal.connect(self._execWidget)  # type: ignore
        self._callback = rt.NodeEventCallback(all=self._execNode)
        self._execNode()

    def _execNode(self, *args: Any) -> None:
        """Called when the node triggers an event callback. Updates the slot on the
        QWidget object.

        Args:
            event (rt.Name): Unused
            nodes (List[int]): Unused
        """
        if hasattr(self._node, self._prop):
            value = getattr(self._node, self._prop)
            self._slot(value)  # type: ignore
        else:
            self._unbind()

    def _execWidget(self, value: Any) -> None:
        """Called when the QWidget object emits the signal. Updates the nodes attribute
        with the new value.

        Args:
            value (Any): The value emitted from the signal.
        """
        setattr(self._node, self._prop, value)
        rt.RedrawViews()

    def _unbind(self) -> None:
        """Unbinds (deconstructs) the NodeEventCallback."""
        self._callback = None


class AutoWindow(QMainWindow):
    """Window with convenience features already setup.

    - Auto-load/save widget properties
    - Load .ui file
    - Kill instances of this window upon launch (ensuring
    only one instance of this window exists)
    """

    _uniqueName: str
    _uiFileName: str
    _settings: QSettings
    _bindings: List[Binding]

    def __init__(
        self,
        title: str,
        parent: QWidget = maxhwnd,
        uiFileName: str = "",
        unique: bool = True,
    ) -> None:
        super().__init__(parent)

        # Window title, name
        self.setWindowTitle(title)
        self._uniqueName = self.__class__.__name__
        self.setObjectName(self._uniqueName)

        # Settings
        self._settings = QSettings(self._uniqueName, self._uniqueName)

        # GUI setup
        self._uiFileName = uiFileName
        self._setupUi()

        # Connection and binding setup
        self._setupConnections()
        self._bindings = []

        # Close instances if this window should be unique
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
        for binding in reversed(self._bindings):
            del binding
        super().closeEvent(event)

    def _setupUi(self) -> None:
        """Setup GUI from .ui file or set the central widget to a plain QWidget.

        Manually adding widgets to this window should be done by overriding
        this method.

        Usage::
        ```python
        class MyWindow(AutoWindow):
            ...
            def _setupUi(self) -> None:
                super()._setupUi()
                self.btn = QPushButton()
                self.ui.layout().addWidget(self.btn)
        ```
        """
        if self._uiFileName != "":
            loader = QUiLoader()
            filename = fileio.relative(f"..\\tools\\{self._uiFileName}.ui")

            if not os.path.exists(filename):
                raise FileNotFoundError(f"File {filename} not found!")

            file = QFile(filename)
            file.open(QFile.ReadOnly)

            self.ui = loader.load(file, self.parent())

            file.close()
        else:
            self.ui = QWidget()

        self.setCentralWidget(self.ui)

    @abc.abstractmethod
    def _setupConnections(self) -> None:
        pass

    def bind(
        self, signal: Signal, slot: Callable[[Any], None], node: rt.Node, prop: str
    ) -> None:
        """Bind a QWidget object to a 3ds Max node property and vice versa.

        Args:
            signal (Signal): The signal emitted from the widget.
            slot (Callable): The method (slot) to set the widget's value.
            node (rt.Node): The node to bind the widget to.
            prop (str): The node's property name to bind to.

        Usage::
        ```python
        spn = QSpinBox()
        sphere = rt.Sphere()
        self.bind(spn.valueChanged, spn.setValue, sphere, "radius")
        ```
        """
        binding = Binding(signal, slot, node, prop)
        self._bindings.append(binding)

    def closeInstances(self) -> None:
        """Close all instances of this window."""
        if self.parentWidget() is None:
            return

        dialogs = self.parentWidget().findChildren(QMainWindow, self._uniqueName)
        for dialog in dialogs:
            if dialog.isVisible():
                dialog.close()

    def readSettings(self) -> None:
        pos = self._settings.value("pos", QSize(0, 0))
        self.move(pos)  # type: ignore

        size = self._settings.value("size", QSize(640, 480))
        self.resize(size)  # type: ignore

    def writeSettings(self) -> None:
        self._settings.setValue("pos", self.pos())
        self._settings.setValue("size", self.size())

    @abc.abstractmethod
    def addCallbacks(self) -> None:
        pass

    @abc.abstractmethod
    def deleteCallbacks(self) -> None:
        pass
