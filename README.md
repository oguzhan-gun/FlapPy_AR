# Gesture Controlled Flappy Bird

A real-time gesture controlled Flappy Bird project developed using Python, OpenCV, MediaPipe, and Pygame.

The project extends the original FlapPyBird implementation by integrating a real-time hand tracking and gesture recognition system for controlling the bird without keyboard input.

## Features

* Real-time hand tracking using MediaPipe
* Gesture-based bird control
* OpenCV visualization
* Pygame game integration
* Real-time computer vision interaction

## Demo

[Demo Video](./demo.mp4)

## Controls

* Move your hand upward quickly to trigger a flap action
* Press `ESC` to quit the application

## Requirements

* Python 3.10+
* OpenCV
* MediaPipe `0.10.20`
* Pygame

Install dependencies:

```bash id="w9g6c2"
pip install mediapipe==0.10.20
pip install opencv-python
pip install pygame
```

## Run

```bash
python main.py
```

## Project Structure

```text
FlapPyBird/
├── main.py
├── src/
│   ├── flappy.py
│   ├── entities/
│   │   └── RealTimeControllerHands.py
```

## Technologies

* Python
* OpenCV
* MediaPipe
* Pygame
* Computer Vision

## Credits

Base Flappy Bird implementation adapted from:

https://github.com/sourabhv/FlapPyBird

Original FlapPyBird project developed by Sourabh Verma.

This project extends the original game with a real-time gesture-based interaction system using MediaPipe and OpenCV.

