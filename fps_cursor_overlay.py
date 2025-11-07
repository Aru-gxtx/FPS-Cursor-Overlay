import sys
import os

from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen
from PyQt6.QtCore import Qt, QSize

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class OverlayWindow(QMainWindow):
    def __init__(self, pixmap, screen_geometry):
        super().__init__()
        self.pixmap = pixmap
        self.screen_geo = screen_geometry
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.WindowTransparentForInput
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.label = QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.label)
        self.resize(self.pixmap.width(), self.pixmap.height())
        self.center_window()

    def center_window(self):
        screen_width = self.screen_geo.width()
        screen_height = self.screen_geo.height()
        window_width = self.width()
        window_height = self.height()
        center_x = (screen_width - window_width) // 2
        center_y = (screen_height - window_height) // 2
        
        vertical_offset = window_height // 2
        new_center_y = center_y + vertical_offset
        
        self.move(center_x, new_center_y)

def main():
    image_file = resource_path("overlay.png")

    app = QApplication(sys.argv)
    
    pixmap = QPixmap(image_file)

    original_width = pixmap.width()
    original_height = pixmap.height()
    new_width = int(original_width * 0.05)
    new_height = int(original_height * 0.05)
    new_width = max(1, new_width)
    new_height = max(1, new_height)
    print(f"Resizing image from {original_width}x{original_height} -> {new_width}x{new_height}")
    pixmap = pixmap.scaled(
        new_width, 
        new_height, 
        Qt.AspectRatioMode.KeepAspectRatio, 
        Qt.TransformationMode.SmoothTransformation
    )

    primary_screen = QApplication.primaryScreen()
    if not primary_screen:
        print("Error: Could not detect a primary screen.")
        sys.exit(-1)
        
    screen_geometry = primary_screen.geometry()
    overlay = OverlayWindow(pixmap, screen_geometry)
    overlay.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
