# Multi-Widget Repository

This repository contains a collection of custom PyQt5 widgets. Currently, it includes a transparent clock widget, but additional widgets will be added in the future.

## Current Widget

### Transparent Clock Widget (`clock.py`)

The `clock.py` widget is a transparent, frameless clock that displays the current time and date with a custom font. It has the following features:

- **Customizable Font**: The clock can display a custom font (default is "Arial" if no custom font is provided).
- **Real-Time Update**: The time and date are updated every second.
- **Transparent Background**: The widget has a translucent background with rounded corners.
- **Position**: Initially placed at the top-right corner of the screen.
- **Close Button**: A hidden close button appears when the mouse hovers over the clock's area.
- **Draggable**: The clock widget can be moved around the screen by clicking and dragging.

## Screenshots
![Clock](https://imgur.com/ZYPijfD.png)

### Requirements

- Python 3.x
- PyQt5

You can install PyQt5 using `pip`:
```bash
pip install pyqt5
```

## Usage
1. Clone this repository to your local machine.
2. Navigate to the directory where the clock.py file is located.
3. Run the script:
 ```bash
 python clock.py
 ```
 This will launch the transparent clock widget on your screen.

## Adding More Widgets
In the future, additional widgets will be added to this repository. Each widget will be implemented as a separate Python file under the same repository. You can easily import and use these widgets in your own PyQt5 applications.

## Contributing
Feel free to submit issues or pull requests if you have suggestions or improvements for any of the widgets. Contributions are welcome!

## License
This project is licensed under the MIT License - see the LICENSE file for details.