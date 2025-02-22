import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QSystemTrayIcon, QMenu, QAction, QLabel
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor

class WidgetLauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Desktop Widget Launcher")
        self.setWindowIcon(QIcon("images/icon.png"))
        self.setGeometry(100, 100, 400, 300)
        self.initUI()
        self.create_tray_icon()

    def initUI(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(45, 45, 45))
        self.setPalette(palette)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("Widget Launcher")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white;")
        layout.addWidget(title)

        self.weather_button = self.create_button("Weather Widget", "weather.py")
        self.time_button = self.create_button("Time & Date Widget", "clock.py")
        self.music_button = self.create_button("Music Player Widget", "mplayer.py")

        layout.addWidget(self.weather_button)
        layout.addWidget(self.time_button)
        layout.addWidget(self.music_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.setStyleSheet("background-color: #2d2d2d;")

    def create_button(self, text, script_name):
        button = QPushButton(text)
        button.setFont(QFont("Arial", 12))
        button.setFixedHeight(40)
        button.setStyleSheet(
            "QPushButton {"
            "background-color: #444;"
            "color: white;"
            "border-radius: 10px;"
            "padding: 5px;"
            "}"
            "QPushButton:hover {"
            "background-color: #666;"
            "}"
        )
        button.clicked.connect(lambda: self.launch_widget(script_name))
        return button

    def launch_widget(self, script_name):
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_name)
        if os.path.exists(script_path):
            subprocess.Popen([sys.executable, script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            print(f"Error: {script_name} not found")

    def create_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(QIcon("images/icon.png"), self)
        self.tray_icon.setToolTip("Widget Launcher")

        tray_menu = QMenu()
        restore_action = QAction("Open Launcher", self)
        restore_action.triggered.connect(self.show)
        tray_menu.addAction(restore_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.exit_application)
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_click)
        self.tray_icon.show()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Widget Launcher",
            "Launcher minimized to system tray.",
            QSystemTrayIcon.Information,
            3000,
        )

    def on_tray_icon_click(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show()

    def exit_application(self):
        self.tray_icon.hide()
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = WidgetLauncher()
    launcher.show()
    sys.exit(app.exec_())
