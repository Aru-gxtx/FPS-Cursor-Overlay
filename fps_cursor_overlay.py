import sys
import os
import random
from pynput import mouse, keyboard  # Added keyboard support

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import (
    Qt, pyqtSignal, QThread, 
    QPropertyAnimation, pyqtProperty, QEasingCurve, QTimer
)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class GlobalMouseWorker(QThread):
    mouse_state_changed = pyqtSignal(bool)

    def run(self):
        with mouse.Listener(on_click=self.on_click) as listener:
            listener.join()

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.left:
            self.mouse_state_changed.emit(pressed)

class GlobalKeyboardWorker(QThread):
    kill_signal = pyqtSignal()

    def run(self):
        with keyboard.Listener(on_release=self.on_release) as listener:
            listener.join()

    def on_release(self, key):
        if key == keyboard.Key.f10:
            self.kill_signal.emit()
            return False # Stop listener

class OverlayWindow(QMainWindow):
    def __init__(self, pixmap, screen_geometry):
        super().__init__()
        self.original_pixmap = pixmap
        self.screen_geo = screen_geometry
        
        self._scale_factor = 1.0
        self.base_width = pixmap.width()
        self.base_height = pixmap.height()
        
        self.window_width = int(self.base_width * 1.2)
        self.window_height = int(self.base_height * 1.2)
        
        self.anim = QPropertyAnimation(self, b"scale_factor")
        
        self.pulse_timer = QTimer()
        self.pulse_timer.setInterval(100)
        self.pulse_timer.timeout.connect(self.trigger_pulse_cycle)

        self.init_ui()
        self.start_listeners()

    def init_ui(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.WindowTransparentForInput |
            Qt.WindowType.Tool 
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(self.window_width, self.window_height)
        self.center_window()

    def center_window(self):
        screen_width = self.screen_geo.width()
        screen_height = self.screen_geo.height()
        center_x = (screen_width - self.width()) // 2
        center_y = (screen_height - self.height()) // 2
        self.move(center_x, center_y)

    def start_listeners(self):
        self.mouse_worker = GlobalMouseWorker()
        self.mouse_worker.mouse_state_changed.connect(self.handle_mouse_event)
        self.mouse_worker.start()

        self.key_worker = GlobalKeyboardWorker()
        self.key_worker.kill_signal.connect(self.close_application)
        self.key_worker.start()

    def close_application(self):
        print("Kill switch activated. Closing...")
        QApplication.quit()

    def get_scale_factor(self):
        return self._scale_factor

    def set_scale_factor(self, factor):
        self._scale_factor = factor
        self.update()

    scale_factor = pyqtProperty(float, get_scale_factor, set_scale_factor)

    def handle_mouse_event(self, pressed):
        if pressed:
            if not self.pulse_timer.isActive():
                self.pulse_timer.start()
                self.trigger_pulse_cycle()
        else:
            self.pulse_timer.stop()
            self.reset_to_normal()

    def trigger_pulse_cycle(self):
        peak_size = random.choice([1.09, 1.10, 1.11])
        self.anim.stop()
        self.anim.setDuration(90)
        self.anim.setKeyValues([
            (0.0, 1.0),
            (0.5, peak_size),
            (1.0, 1.0)
        ])
        self.anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.anim.start()

    def reset_to_normal(self):
        self.anim.stop()
        self.anim.setDuration(50)
        self.anim.setStartValue(self._scale_factor)
        self.anim.setEndValue(1.0)
        self.anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        current_w = self.base_width * self._scale_factor
        current_h = self.base_height * self._scale_factor
        
        x = (self.width() - current_w) / 2
        y = (self.height() - current_h) / 2
        
        target_rect = [int(x), int(y), int(current_w), int(current_h)]
        painter.drawPixmap(target_rect[0], target_rect[1], target_rect[2], target_rect[3], self.original_pixmap)
        painter.end()

def main():
    image_file = resource_path("overlay.png")
    app = QApplication(sys.argv)

    pixmap = QPixmap(image_file)

    original_width = pixmap.width()
    original_height = pixmap.height()
    new_width = int(original_width * 0.25)
    new_height = int(original_height * 0.25)
    
    pixmap = pixmap.scaled(
        new_width, new_height,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation
    )

    primary_screen = QApplication.primaryScreen()
    screen_geometry = primary_screen.geometry()
    
    overlay = OverlayWindow(pixmap, screen_geometry)
    overlay.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
