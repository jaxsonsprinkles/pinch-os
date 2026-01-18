# PinchOS

A hand gesture-based window management system for Windows that uses computer vision to control your desktop windows with pinch gestures.

## Overview

PinchOS allows you to move windows on your Windows desktop by pinching your thumb and index finger together while pointing at a window. The system uses your webcam to track hand movements in real-time and displays an interactive overlay showing available windows.

## Requirements

- Python 3.x
- Windows OS (uses win32api and win32gui)
- Webcam

## Dependencies

```
opencv-python
mediapipe
pygame
pywin32
screeninfo
```

## Installation

1. Clone this repo
2. Install requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```
3. Download the MediaPipe hand landmarker model file
   `wget -q https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task`

## Usage

Run the main application:

```bash
python main.py
```

### Controls

- Show your hand to the webcam
- A green pointer will appear at your index finger tip
- The top 3 windows will be highlighted with green borders
- Pinch your thumb and index finger together while pointing at a window to grab it
- Move your hand while pinching to drag the window
- Release the pinch to drop the window
- Press `q` to quit the application

## How It Works

### Components

**main.py**: The main application loop that captures webcam video, processes hand detection, and coordinates between the gesture recognition and overlay systems

**pinchos.py**: Handles hand landmark detection and pinch gesture recognition. Calculates the distance between thumb and index finger tips to determine pinch state

**overlay.py**: Creates a transparent pygame overlay window that displays window boundaries and the hand pointer. Manages window enumeration and movement

**constants.py**: Stores landmark indices and screen dimensions

## License

See `LICENSE.txt`

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

Made by Jaxson Sprinkles in 3 days
