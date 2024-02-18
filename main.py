#!/bin/env python3

import signal
import sys
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPainter, QBrush, QColor, QCursor, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout

class TransparentWindow(QWidget):
    def __init__(self, x=300, y=300, width=1280, height=720, border=1):
        super().__init__()

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border = border

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setGeometry(x, y, width, height)
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw a transparent background
        painter.setBrush(QBrush(QColor(0, 0, 0, 0)))
        painter.drawRect(self.rect())

    def grab_screen(self):
        screen = QApplication.primaryScreen()

        mouse_coords = QCursor.pos()

        # offset the mouse position
        mouse_point = QPoint(mouse_coords.x() - self.x - 8, mouse_coords.y() - self.y - 8)

        return screen.grabWindow(0, self.x + self.border, self.y + self.border, self.width - self.border, self.height - self.border), mouse_point


class MirrorWindow(QMainWindow):

    def __init__(self, orignal_window):
        super().__init__()

        # set title
        self.setWindowTitle("Mirror Window")

        self.original_window = orignal_window

        self.setGeometry(self.original_window.x + self.original_window.width + 10, self.original_window.y, self.original_window.width, self.original_window.height)

        self.label = QLabel(self)
        self.label.setStyleSheet("border: none;")

        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout(self.widget)
        self.layout.addWidget(self.label)

        #self.mouse_pointer_image = QPixmap("mouse_pointer2.png")
        self.mouse_pointer_image = QPixmap("/usr/share/icons/breeze-dark/actions/32/tool-pointer.svg")
        self.show()

    def paintEvent(self, event):
        screenshot, mouse_pos = self.original_window.grab_screen()

        painter = QPainter(screenshot)
        painter.drawPixmap(mouse_pos, self.mouse_pointer_image)
        painter.end()

        self.label.setPixmap(screenshot)


def handle_sigint(*args):
    QApplication.quit()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = TransparentWindow()

    mirror = MirrorWindow(window)


    signal.signal(signal.SIGINT, handle_sigint)

    # Start a timer to check for KeyboardInterrupt every 500ms
    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)


    sys.exit(app.exec_())
