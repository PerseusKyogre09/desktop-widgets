from PyQt5.QtCore import QTimer, Qt, QDateTime
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QSystemTrayIcon, QMenu, QPushButton
from PyQt5.QtGui import QIcon
import sys
import os

class DraggableWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window to be frameless and translucent
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 120); border-radius: 15px;")

        # Layout and time label setup
        main_layout = QVBoxLayout(self)
        self.time_date_label = QLabel("Loading Time...", self)
        self.time_date_label.setStyleSheet("color: white; font-size: 24px;")
        main_layout.addWidget(self.time_date_label)

        # Close button
        self.close_button = QPushButton("X", self)
        self.close_button.setStyleSheet("background-color: transparent; color: white; font-size: 16px; border: none;")
        self.close_button.clicked.connect(self.hide_to_tray)
        main_layout.addWidget(self.close_button, alignment=Qt.AlignRight)  # Align close button to the right

        # Timer to update time
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

        # System tray icon setup
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("images/clock_icon.png"))
        self.tray_icon.setToolTip("Clock Widget")

        # Tray menu setup
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
        self.tray_icon.show()

        # Initialize the position tracking variable
        self.old_pos = None

    def hide_to_tray(self):
        self.hide()
        # Shows message when closed
        self.tray_icon.showMessage(
            "Transparent Clock",
            "The Clock widget has been minimized to the system tray.",
            QSystemTrayIcon.Information,
            3000
        )

    def update_time(self):
        current_time = QDateTime.currentDateTime()
        # formatted_time = current_time.toString("hh:mm AP\ndddd, MMMM dd, yyyy")
        hour = current_time.toString("hh")
        minute = current_time.toString("mm")
        am_pm = current_time.toString("AP")
        date_text = current_time.toString("dddd, MMMM dd, yyyy")

        # display_text = f"""
        #     <div style="text-align: center;">
        #         <span style="font-size: 70px;">{hour}:{minute}</span><br>
        #         <span style="font-size: 70px;">{am_pm}</span><br>
        #         <span style="font-size: 30px;">{date_text}</span>
        #     </div>
        # """

        # self.time_date_label.setText(display-text)
        display_text = f"{hour}:{minute}\n{am_pm}\n{date_text}"
        self.time_date_label.setText(display_text)


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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DraggableWindow()
    window.resize(300, 200)
    window.move(1440, 0)
    window.show()
    sys.exit(app.exec_())
