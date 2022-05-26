import importlib

from bettermaxtools import MAX_HWND
from bettermaxtools.utils import cameras, lighting, maxscript
from bettermaxtools.widgets.autowindow import AutoWindow
from PySide2.QtWidgets import QFrame, QMessageBox, QPushButton, QVBoxLayout

importlib.reload(lighting)
importlib.reload(maxscript)
importlib.reload(lighting)


class IconRendererWindow(AutoWindow):
    def __init__(self):
        super().__init__("Icon Renderer")
        self.importLightRigBtn = QPushButton("Import Light Rig")
        self.importLightRigBtn.clicked.connect(self.on_light_rig_btn_clicked)

        self.alignCameraBtn = QPushButton("Align camera")
        self.alignCameraBtn.clicked.connect(self.on_align_camera_btn_clicked)

        layout = QVBoxLayout()
        layout.addWidget(self.importLightRigBtn)
        layout.addWidget(self.alignCameraBtn)

        frame = QFrame()
        frame.setLayout(layout)
        self.setCentralWidget(frame)

    def on_light_rig_btn_clicked(self):
        if not lighting.does_rig_exist():
            print("No rig found - importing!")
            lighting.import_light_rig()
        else:
            print("Rig found - not importing!")
            QMessageBox.warning(MAX_HWND, "Import", "Light rig already found in scene.")

    def on_align_camera_btn_clicked(self):
        selected = maxscript.get_current_selection()
        selected.pos = maxscript.rt.Point3(0, 0, 0)
        camera = cameras.create_camera()
        camera.fov = 12.5
        cameras.align_camera(camera, selected)
        cameras.set_viewport_camera(camera)
        maxscript.redraw()


if __name__ == "__main__":
    w = IconRendererWindow()
    w.show()
