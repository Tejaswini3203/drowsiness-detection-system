# Drowsiness Detection System

A beginner-friendly Python computer-vision project that uses a webcam and OpenCV to detect a face and eyes. If the eyes are not detected for several consecutive frames, the app displays a warning and plays a beep on Windows.

> **Important limitation:** This is an educational prototype, not a reliable driver-safety system or medical device. Haar-cascade eye detection can produce false alarms and can miss drowsiness. Do not use it as the only protection while driving.

## Features

- Live webcam feed
- Face detection using OpenCV Haar cascades
- Eye detection and visual rectangles
- Warning after repeated frames where eyes are not detected
- Beep alert on Windows
- Press `Q` to exit

## Requirements

- Python 3.9 or newer
- A working webcam
- Internet connection for installing OpenCV

## Setup on Windows

1. Install Python from [python.org](https://www.python.org/downloads/). During setup, select **Add Python to PATH**.
2. Download or clone this repository.
3. Open Command Prompt or the VS Code terminal inside the project folder.
4. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

5. Activate it:

   ```bash
   venv\\Scripts\\activate
   ```

6. Install the dependency:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

7. Run the project:

   ```bash
   python main.py
   ```

8. Look toward the webcam. Press `Q` in the camera window to stop.

## Run on macOS or Linux

Create and activate a virtual environment, install the requirements with `pip install -r requirements.txt`, then run `python main.py`. On non-Windows systems, the warning is printed in the terminal instead of playing a beep.

## How it works

1. OpenCV captures frames from the webcam.
2. Each frame is converted to grayscale.
3. Haar-cascade classifiers detect a face and eyes.
4. If fewer than two eyes are detected for a configured number of frames, the app shows a possible-drowsiness warning.
5. On Windows, a beep is played periodically while the warning remains active.

## Configuration

Open `main.py` and change:

- `CAMERA_INDEX = 0` if your webcam uses a different camera index.
- `CLOSED_EYE_FRAME_LIMIT = 20` to change how long the eye-detection signal must persist before the warning.
- `ALARM_INTERVAL_SECONDS = 2.0` to change the interval between beeps.

A higher frame limit can reduce some false alarms, but this approach is still only a simple demonstration.

## Troubleshooting

- **Camera will not open:** Close other camera apps and check Windows camera permissions.
- **No sound:** The beep uses Python's Windows `winsound` module. On macOS/Linux the program prints the warning instead.
- **Too many false alarms:** Improve lighting, face the camera, remove obstructions, and experiment with `CLOSED_EYE_FRAME_LIMIT`.
- **Module not found:** Activate the virtual environment and run `pip install -r requirements.txt`.

## Project structure

```text
drowsiness-detection-system/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Technologies

- Python
- OpenCV
- Computer Vision
- Haar Cascade Classifiers

## Future improvements

- Use facial landmarks and Eye Aspect Ratio (EAR) for more robust eye-closure estimation.
- Add yawning detection.
- Save timestamped alert events to a CSV file.
- Add a dashboard to visualize alerts and session statistics.
- Evaluate precision, recall, and false-alarm rate on a labeled dataset.

## License

This project is provided for learning and educational use.
