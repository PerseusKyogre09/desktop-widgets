import sys
import vlc
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QMenu, QSystemTrayIcon, QHBoxLayout, QProgressBar, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QTime, QTimer, QPoint, QSize, QPropertyAnimation
from PyQt5.QtGui import QMouseEvent, QFont, QIcon, QFontDatabase

class TransparentMusicPlayer(QWidget):
    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowFlags(Qt.WindowStaysOnBottomHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.9)
        self.setGeometry(100, 100, 300, 200)

        # Custom font
        font_id = QFontDatabase.addApplicationFont("fonts/minecraft.ttf")
        if font_id != -1 and QFontDatabase.applicationFontFamilies(font_id):
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.custom_font = QFont(font_family, 24)
        else:
            self.custom_font = QFont("Arial", 24)

        # Layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.setStyleSheet(""" 
            QWidget {
                background-color: rgba(0, 0, 0, 180);
                color: white;
                border-radius: 10px;
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
        """)

        # Minimize to tray button
        self.minimize_to_tray_button = QPushButton(self)
        self.minimize_to_tray_button.setIcon(QIcon("images/close_icon.png"))
        self.minimize_to_tray_button.setIconSize(QSize(24, 24))
        self.minimize_to_tray_button.setStyleSheet("background-color: transparent; border: none;")
        self.minimize_to_tray_button.clicked.connect(self.hide_to_tray)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.minimize_to_tray_button, alignment=Qt.AlignRight)
        main_layout.addLayout(button_layout)

        # VLC player 
        self.player = vlc.MediaPlayer()
        
        # Music name label
        self.music_name_label = QLabel("No Music Loaded")
        self.music_name_label.setFont(self.custom_font)
        self.music_name_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.music_name_label)
        
        # Blinking opacity
        self.opacity_effect = QGraphicsOpacityEffect(self.music_name_label)
        self.music_name_label.setGraphicsEffect(self.opacity_effect)
        
        # Blinking animation
        self.blink_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.blink_animation.setDuration(2000)
        self.blink_animation.setStartValue(0.3)
        self.blink_animation.setEndValue(1.0)
        self.blink_animation.setLoopCount(-1)

        # Time on Music
        self.duration_label = QLabel("00:00 / 00:00")
        self.duration_label.setFont(self.custom_font)
        self.duration_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.duration_label)

        # Progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #333;
                border: 1px solid #555;
                height: 8px;
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background-color: #777;
                border-radius: 5px;
            }
        """)
        main_layout.addWidget(self.progress_bar)

        # Play button
        self.play_button = QPushButton(self)
        self.play_button.setIcon(QIcon("images/play_icon.jpeg"))
        self.play_button.setIconSize(QSize(48, 48))
        self.play_button.setStyleSheet("background-color: transparent; border: none;")
        self.play_button.clicked.connect(self.toggle_play_pause)

        # Stop button
        self.stop_button = QPushButton(self)
        self.stop_button.setIcon(QIcon("images/stop_icon.png"))
        self.stop_button.setIconSize(QSize(48, 48))
        self.stop_button.setStyleSheet("background-color: transparent; border: none;")
        self.stop_button.clicked.connect(self.stop_music)

        # Load button
        load_button = QPushButton(self)
        load_button.setIcon(QIcon("images/load_icon.png"))
        load_button.setIconSize(QSize(48, 48))
        load_button.setStyleSheet("background-color: transparent; border: none;")
        load_button.clicked.connect(self.load_music)

        # Layout for buttons
        control_button_layout = QHBoxLayout()
        control_button_layout.addWidget(self.play_button)
        control_button_layout.addWidget(self.stop_button)
        control_button_layout.addWidget(load_button)
        main_layout.addLayout(control_button_layout)

        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.total_duration = QTime(0, 0, 0)

        # Tray icon
        self.tray_icon = QSystemTrayIcon(QIcon("images/music.png"), self)
        self.tray_icon.setToolTip("Music Player")

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
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()
        self.old_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPos() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPos()

    def load_music(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open Music File", "", "Audio Files (*.mp3 *.wav *.ogg)")
        if file_path:
            self.player.set_mrl(file_path)
            self.music_name_label.setText(os.path.splitext(os.path.basename(file_path))[0])
            self.play_button.setIcon(QIcon("images/play_icon.jpeg"))
            self.duration_label.setText("00:00 / 00:00")
            self.progress_bar.setValue(0)
            self.progress_bar.setVisible(True)
            self.total_duration = QTime(0, 0, 0)

            self.player.play()
            QTimer.singleShot(100, self.player.pause)

    def toggle_play_pause(self):
        if self.player.is_playing():
            self.player.pause()
            self.play_button.setIcon(QIcon("images/play_icon.jpeg"))
            self.blink_animation.start()  # Start blinking
        else:
            self.player.play()
            self.play_button.setIcon(QIcon("images/pause_icon.png"))
            self.blink_animation.stop()  # Stop blinking
            self.opacity_effect.setOpacity(1.0)
            self.timer.start(1000)

    def stop_music(self):
        self.player.stop()
        self.play_button.setIcon(QIcon("images/play_icon.jpeg"))
        self.music_name_label.setText("No Music Loaded")
        self.duration_label.setText("00:00 / 00:00")
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        self.timer.stop()
        self.blink_animation.stop()
        self.opacity_effect.setOpacity(1.0)

    def update_position(self):
        current_time_sec = int(self.player.get_time() / 1000)
        total_time_sec = int(self.player.get_length() / 1000)

        current_time = QTime(0, (current_time_sec // 60) % 60, current_time_sec % 60)
        total_time = QTime(0, (total_time_sec // 60) % 60, total_time_sec % 60)

        self.duration_label.setText(f"{current_time.toString('mm:ss')} / {total_time.toString('mm:ss')}")
        
        if total_time_sec > 0:
            progress_value = (current_time_sec / total_time_sec) * 100
            self.progress_bar.setValue(int(progress_value))

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show()
            self.activateWindow()

    def hide_to_tray(self):
        self.hide()
        self.tray_icon.showMessage(
            "Transparent Music Player",
            "The music player has been minimized to the system tray.",
            QSystemTrayIcon.Information,
            3000,
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = TransparentMusicPlayer()
    player.show()
    sys.exit(app.exec_())
