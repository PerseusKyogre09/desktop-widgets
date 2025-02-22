import sys
import os
import requests
from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QSystemTrayIcon, QMenu, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QColor, QFont, QFontDatabase, QPalette, QIcon, QMovie

load_dotenv()
API_KEY = os.getenv('API_KEY')

def get_user_city():
    try:
        geo_response = requests.get('https://ipinfo.io')
        if geo_response.status_code == 200:
            geo_data = geo_response.json()
            return geo_data.get('city', 'London')
    except Exception as e:
        print("Error fetching location:", e)
    return 'London'

def load_custom_font():
    font_path = os.path.join("fonts", "minecraft.ttf")
    if os.path.exists(font_path):
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            return QFont(font_family)
    return QFont("Arial")

class WeatherWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.city = get_user_city()
        self.api_url = f'http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={API_KEY}&units=metric'
        self.custom_font = load_custom_font()
        self.initUI()
        self.get_weather()
        self.setup_timer()
        self.start_pos = None

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnBottomHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 120); border-radius: 15px;")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()
        
        self.weather_gif_label = QLabel(self)
        self.weather_gif_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.weather_gif_label)
        
        self.weather_desc = QLabel("Loading...", self)
        self.weather_desc.setFont(self.custom_font)
        self.weather_desc.setStyleSheet("color: white; font-size: 18px;")
        layout.addWidget(self.weather_desc, alignment=Qt.AlignCenter)
        
        self.temperature = QLabel("", self)
        self.temperature.setFont(self.custom_font)
        self.temperature.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        layout.addWidget(self.temperature, alignment=Qt.AlignCenter)

        self.setLayout(layout)

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.opacity_effect.setOpacity(0.01)
        
        self.close_button = QPushButton("X", self)
        self.close_button.setGraphicsEffect(self.opacity_effect)
        self.close_button.setStyleSheet("background-color: transparent; color: white; font-size: 24px; border: none;")
        self.close_button.clicked.connect(self.hide_to_tray)
        layout.addWidget(self.close_button, alignment=Qt.AlignCenter)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("images/weather_icon.png"))
        self.tray_icon.setToolTip("Weather Widget")

        tray_menu = QMenu()
        show_action = tray_menu.addAction("Show")
        show_action.triggered.connect(self.show)
        exit_action = tray_menu.addAction("Exit")
        exit_action.triggered.connect(QApplication.quit)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_left_click)
        self.tray_icon.show()

    def setup_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.get_weather)
        self.timer.start(600000)

    def get_weather(self):
        try:
            response = requests.get(self.api_url)
            if response.status_code == 200:
                data = response.json()
                weather = data['weather'][0]['main']
                temp = data['main']['temp']
                self.update_ui(weather, temp)
            else:
                self.weather_desc.setText("Error fetching weather")
        except Exception as e:
            print("Network error:", e)
            self.weather_desc.setText("Error fetching weather")

    def update_ui(self, weather, temp):
        self.temperature.setText(f"{temp}°C")
        self.weather_desc.setText(weather)

        gif_path = self.get_gif_path(weather)
        if gif_path and os.path.exists(gif_path):
            self.display_weather_gif(gif_path)

    def get_gif_path(self, weather):
        weather_conditions = {
            "Clear": "images/weather/clear/sunny.gif",
            "Clouds": "images/weather/cloudy/cloudy.gif",
            "Rain": "images/weather/rain/moderate_rain.gif",
            "Drizzle": "images/weather/drizzle/drizzle.gif",
            "Thunderstorm": "images/weather/thunderstorm/thunderstorm.gif",
            "Snow": "images/weather/snow/snow.gif",
            "Mist": "images/weather/haze/fog.gif",
            "Smoke": "images/weather/haze/haze.gif",
            "Haze": "images/weather/haze/haze.gif",
            "Dust": "images/weather/haze/haze.gif",
            "Fog": "images/weather/haze/fog.gif",
            "Sand": "images/weather/haze/haze.gif",
            "Ash": "images/weather/haze/haze.gif",
            "Squall": "images/weather/windy/windy.gif",
            "Tornado": "images/weather/tornado/tornado.gif"
        }
        return weather_conditions.get(weather, "images/weather/clear/sunny.gif")

    def display_weather_gif(self, gif_path):
        gif = QMovie(gif_path)
        self.weather_gif_label.setMovie(gif)
        gif.start()

    def hide_to_tray(self):
        self.hide()
        self.tray_icon.showMessage(
            "Weather Widget",
            "Weather widget minimized to system tray.",
            QSystemTrayIcon.Information,
            3000,
        )

    def on_tray_icon_left_click(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show()

    def enterEvent(self, event):
        self.opacity_effect.setOpacity(1)

    def leaveEvent(self, event):
        self.opacity_effect.setOpacity(0.01)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.start_pos:
            self.move(event.globalPos() - self.start_pos)
            event.accept()

def run_weather():
    app = QApplication(sys.argv)
    widget = WeatherWidget()
    widget.show()
    widget.move(1440, 0)
    app.exec_()

if __name__ == '__main__':
    run_weather()
