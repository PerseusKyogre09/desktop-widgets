from PyQt5.QtCore import QTimer, Qt, QDateTime, QPoint, QSize
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QFontDatabase, QFont, QCursor, QIcon
import sys
import os

class TransparentClockWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 120); border-radius: 15px;")

        # Load custom font
        font_path = "fonts/minecraft.ttf"
        if os.path.exists(font_path):
            font_id = QFontDatabase.addApplicationFont(font_path)
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            font_family = "Arial"  # Default font

        # Layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 30)

        # Time and date
        self.time_date_label = QLabel()
        self.time_date_label.setFont(QFont(font_family, 40))
        self.time_date_label.setStyleSheet("color: white;")
        self.time_date_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.time_date_label)

        # Timer update
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

        # Coordinates
        self.move(1440, 0) 

        # Close button
        self.close_button = QPushButton("X", self)
        self.close_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.close_button.setStyleSheet("background-color: transparent; color: white; border: none;")
        self.close_button.hide()
        self.close_button.clicked.connect(self.hide_to_tray)
        self.close_button.move(0, 20)
        
        # System tray
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("images/clock_icon.png"))
        self.tray_icon.setToolTip("Transparent Clock")
        
        # Tray menu
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
        self.tray_icon.activated.connect(self.on_tray_icon_click)
        self.tray_icon.show()

        # Mouse tracker
        self.setMouseTracking(True)
        self.closeButtonHover = False

    def update_time(self):
        current_time = QDateTime.currentDateTime()
        
        # Formatted time and date
        hour = current_time.toString("hh")
        minute = current_time.toString("mm")
        am_pm = current_time.toString("AP")
        date_text = current_time.toString("dddd, MMMM dd, yyyy")

        display_text = f"""
            <div style="text-align: center;">
                <span style="font-size: 70px;">{hour}:{minute}</span><br>
                <span style="font-size: 70px;">{am_pm}</span><br>
                <span style="font-size: 30px;">{date_text}</span>
            </div>
        """
        self.time_date_label.setText(display_text)
        self.adjustSize()

    def hide_to_tray(self):
        self.hide()
        # Shows message when closed
        self.tray_icon.showMessage(
            "Transparent Clock",
            "The Clock widget has been minimized to the system tray.",
            QSystemTrayIcon.Information,
            3000
        )

    # Opens widget if icon is clicked in tray
    def on_tray_icon_click(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            if not self.isVisible():
                self.show()
                self.activateWindow()

    def mousePressEvent(self, event):
        self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = event.globalPos() - self.old_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPos()
        
    def enterEvent(self, event):
        self.close_button.show()

    def leaveEvent(self, event):
        self.closeButtonHover = False
        self.close_button.hide()

    def closeEvent(self, event):
        self.tray_icon.hide()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    clock_widget = TransparentClockWidget()
    clock_widget.show()
    sys.exit(app.exec_())
