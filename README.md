# Multi-Widget Repository

This repository contains a collection of custom PyQt5 widgets. Currently, it includes a transparent clock widget and a music player, but additional widgets will be added in the future.

## Current Widget

A brand new central Launcher to launch multiple widgets at once! Future plans to have it be a installed application.


### Transparent Clock Widget (`clock.py`) 


The `clock.py` widget is a transparent, frameless clock that displays the current time and date with a custom font. It has the following features:

- **Customizable Font**: The clock can display a custom font (default is "Arial" if no custom font is provided).
- **Real-Time Update**: The time and date are updated every second.
- **Transparent Background**: The widget has a translucent background with rounded corners.
- **Close Button**: A hidden close button appears when the mouse hovers over the clock's area.
- **Draggable**: The clock widget can be moved around the screen by clicking and dragging.
- **Minimize To Tray**: The widget can be minimized to tray when `X` button is clicked.

### Music Player Widget (`mplayer.py`)

The `mplayer.py` widget is a transparent music player that can play music from your local computer by selecting them. It has the following features:

- **Customizable Font**: The M-Player can display a custom font (default is "Arial" if no custom font is provided).
- **Real-Time Timer Update**: The timer for music is updated every second.
- **Transparent Background**: The widget has a translucent background with rounded corners.
- **Buttons**: Buttons provided for Play/Pause, Stop, Load and Close.
- **Draggable**: The widget can be moved around the screen by clicking and dragging.
- **Minimize To Tray**: The widget can be minimized to tray when close button is clicked.
- **Progress Menu**: A progress menu which will update every second according to the time in the music.
- **Name display**: Displays the currently playing music, also blinking if the music is in pause mode.

### Weather Widget (`weather.py`)

The `weather.py` widget is a transparent, draggable weather display that shows real-time weather conditions for a user’s location. It has the following features:

- **Customizable Font**: The Weather widget can display a custom font (default is "Arial" if no custom font is provided).
- **Real-Time Weather Update**: The widget updates the weather every 10 minutes, fetching data from the OpenWeather API.
- **Transparent Background**: The widget has a translucent background with rounded corners, giving it a sleek and modern look.
- **Weather Condition Display**: Displays the current weather condition (e.g., sunny, cloudy, rainy, etc.) and temperature in Celsius.
- **Weather Animation**: Displays a GIF corresponding to the current weather condition (e.g., sunny, rain, snow, etc.).
- **Location Detection**: Automatically detects the user's city based on their IP address.
- **Draggable**: The widget can be moved around the screen by clicking and dragging.
- **Minimize To Tray**: The widget can be minimized to the system tray when the close button is clicked.

## Screenshots

![Launcher](https://imgur.com/FCX4TvH.png)
![Clock](https://imgur.com/N0KZd8s.png)
![Notif](https://imgur.com/bhMrmN4.png)
![Clock Tray](https://imgur.com/HkxfTl9.png)
![M-Player](https://imgur.com/Bp8XXAj.png)
![Weather](https://imgur.com/iCIcO0m.png)

## Videos


https://github.com/user-attachments/assets/115f1f5c-b9ff-4969-80e9-df713a0318a2


### Requirements

Check `requirements.txt`.

You can install PyQt5 using `pip`:
```bash
pip install -r requirements.txt
```

## Usage

1. Clone this repository to your local machine.
2. Navigate to the root directory where the python files are located.
3. Run the script:
 ```bash
 python launcher.py
 ```
 This will launch the Launcher on your screen. You can use it to run multiple widgets at once.

## Adding More Widgets

In the future, additional widgets will be added to this repository. Each widget will be implemented as a separate Python file under the same repository. You can easily import and use these widgets in your own PyQt5 applications.

## Contributing

Feel free to submit issues or pull requests if you have suggestions or improvements for any of the widgets. Contributions are welcome!

<div align="center">
  <a href="https://twitter.com/KyogrePerseus"><img alt="Twitter Follow" src="https://img.shields.io/twitter/follow/KyogrePerseus"></a>
  <a href="https://github.com/PersesKyogre09/desktop-widgets/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-purple"></a>
</div>

### Our Contributors ✨

<a href="https://github.com/PerseusKyogre09/desktop-widgets/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=PerseusKyogre09/desktop-widgets" />
</a>
