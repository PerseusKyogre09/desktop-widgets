import sys
from PyQt5.QtCore import QTimer, Qt, QDateTime
from PyQt5.QtWidgets import (
    QApplication, QLabel, QWidget, QVBoxLayout, 
    QSystemTrayIcon, QMenu, QPushButton, 
    QGraphicsOpacityEffect, QHBoxLayout
)
from PyQt5.QtGui import QIcon, QFont, QFontDatabase

class DraggableWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnBottomHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 120); border-radius: 15px;")

        font_id = QFontDatabase.addApplicationFont("fonts/minecraft.ttf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0] if font_id != -1 else "Arial"

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        self.date_time_label = QLabel("", self)
        self.date_time_font = QFont(font_family, 36)
        self.date_time_label.setFont(self.date_time_font)
        self.date_time_label.setStyleSheet("color: white; text-align: center;")
        self.date_time_label.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(self.date_time_label)

        self.close_button = QPushButton("X", self)
        self.close_button.setStyleSheet("background-color: transparent; color: white; font-size: 36px; border: none;")
        self.close_button.clicked.connect(self.hide_to_tray)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.close_button, alignment=Qt.AlignCenter)
        main_layout.addLayout(button_layout)

        self.opacity_effect = QGraphicsOpacityEffect(self.close_button)
        self.opacity_effect.setOpacity(0.01)
        self.close_button.setGraphicsEffect(self.opacity_effect)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_date_time)
        self.timer.start(1000)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("images/clock_icon.png"))
        self.tray_icon.setToolTip("Clock Widget")

        tray_menu = QMenu()
        tray_menu.setStyleSheet("""
            QMenu {
                background-color: #333;
                border: 1px solid #555;
                padding: 10px;
                border-radius: 10px;
            }
            QMenu::item {
                color: white;
                padding: 8px 20px;
                background-color: transparent;
            }
            QMenu::item:selected {
                background-color: #444;
            }
            QMenu::separator {
                height: 1px;
                background: #666;
                margin: 5px 0;
            }
        """)
        show_action = tray_menu.addAction("Show")
        show_action.triggered.connect(self.show)
        exit_action = tray_menu.addAction("Exit")
        exit_action.triggered.connect(QApplication.quit)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_left_click)

        self.tray_icon.show()
        self.old_pos = None

    def hide_to_tray(self):
        self.hide()
        self.tray_icon.showMessage(
            "Transparent Clock",
            "The Clock widget has been minimized to the system tray.",
            QSystemTrayIcon.Information,
            3000,
        )

    def update_date_time(self):
        current_time = QDateTime.currentDateTime()
        hour = current_time.toString("hh")
        minute = current_time.toString("mm")
        am_pm = current_time.toString("AP")

        day_name = current_time.toString("ddd")
        day_month = current_time.toString("ddMM")
        year = current_time.toString("yy")
        self.date_time_label.setText(f"{hour}:{minute}\n{am_pm}\n{day_name} {day_month} {year}")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.old_pos is not None:
            new_pos = event.globalPos() - self.old_pos
            self.move(new_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = None

    def enterEvent(self, event):
        self.opacity_effect.setOpacity(1)

    def leaveEvent(self, event):
        self.opacity_effect.setOpacity(0.01)

    def on_tray_icon_left_click(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show()

def run_clock():
    app = QApplication(sys.argv)
    window = DraggableWindow()
    window.resize(320, 240)
    window.move(1440, 0)
    window.show()
    app.exec_()

if __name__ == "__main__":
    run_clock()
