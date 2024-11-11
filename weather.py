import sys
import os
import requests
from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QPoint
from PyQt5.QtGui import QColor, QFont, QPalette

load_dotenv()
API_KEY = os.getenv('API_KEY')

# Geolocation API
def get_user_city():
    try:
        geo_response = requests.get('https://ipinfo.io')
        if geo_response.status_code == 200:
            geo_data = geo_response.json()
            return geo_data.get('city', 'London')  # Default
        else:
            print("Geolocation error:", geo_response.text)
    except Exception as e:
        print("Error fetching location:", e)
    return 'London'

# Weather Widget
class WeatherWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.city = get_user_city()
        self.api_url = f'http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={API_KEY}&units=metric'
        self.initUI()
        self.get_weather()
        self.setup_timer()
        self.start_pos = None

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setFixedSize(300, 200)
        layout = QVBoxLayout()
        
        self.weather_desc = QLabel("Loading...", self)
        self.weather_desc.setFont(QFont("Arial", 16))
        self.weather_desc.setStyleSheet("color: white;")
        layout.addWidget(self.weather_desc, alignment=Qt.AlignCenter)
        
        self.temperature = QLabel("", self)
        self.temperature.setFont(QFont("Arial", 24, QFont.Bold))
        self.temperature.setStyleSheet("color: white;")
        layout.addWidget(self.temperature, alignment=Qt.AlignCenter)
        
        self.setLayout(layout)
        self.set_background_color()

    def set_background_color(self):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0, 180))
        self.setPalette(palette)

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
                print("Weather API error:", response.text)
                self.weather_desc.setText("Error fetching weather")
        except Exception as e:
            print("Network error:", e)
            self.weather_desc.setText("Error fetching weather")

    def update_ui(self, weather, temp):
        self.temperature.setText(f"{temp}°C")
        self.weather_desc.setText(weather)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.start_pos is not None and event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.start_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = None
            event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = WeatherWidget()
    widget.show()
    sys.exit(app.exec_())
