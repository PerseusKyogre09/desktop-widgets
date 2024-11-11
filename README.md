# Multi-Widget Repository

This repository contains a collection of custom PyQt5 widgets. Currently, it includes a transparent clock widget and a music player, but additional widgets will be added in the future.

## Current Widget

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
The `weather.py` widget is currently a work in progress. Cannot test it due to issues with OpenWeatherMap API.

## Screenshots
![Clock](https://imgur.com/N0KZd8s.png)
![Notif](https://imgur.com/bhMrmN4.png)
![Clock Tray](https://imgur.com/HkxfTl9.png)
![M-Player](https://imgur.com/Bp8XXAj.png)

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
 python clock.py
 python mplayer.py
 ```
 This will launch the widgets on your screen.

## Adding More Widgets
In the future, additional widgets will be added to this repository. Each widget will be implemented as a separate Python file under the same repository. You can easily import and use these widgets in your own PyQt5 applications.

## Contributing
Feel free to submit issues or pull requests if you have suggestions or improvements for any of the widgets. Contributions are welcome!

## License
This project is licensed under the MIT License - see the LICENSE file for details.