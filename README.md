# VisionArm

Contactless robotic manipulator control system powered by real-time computer vision and embedded hardware.

## Overview
VisionArm translates human hand gestures captured by a standard webcam into physical robotic arm movements without requiring wearables, gloves, or external sensors. Built for accessible STEM education and safe remote manipulation.

## Key Features
* **Contactless Control:** Real-time 3D hand tracking using a standard USB or built-in webcam.
* **Low Latency:** Local frame processing ensures immediate physical response of the manipulator.
* **Accessible Hardware:** Built on low-cost, widely available components (Arduino Uno and standard servo motors).
* **Educational Ready:** Ideal for robotics labs, STEM workshops, and safe manipulation demonstrations.

## Tech Stack
* **Computer Vision & AI:** Python, OpenCV, MediaPipe
* **Hardware & Firmware:** Arduino Uno, C++, Servo Motors
* **Communication:** Serial Port (UART)

## How It Works
1. **Capture:** A webcam streams real-time video frames to the local Python script.
2. **Track:** MediaPipe detects 21 3D hand landmarks and calculates finger states and spatial coordinates.
3. **Transmit:** Positional data is converted into servo angles and sent via Serial communication to the Arduino microcontroller.
4. **Actuate:** The Arduino firmware parses incoming commands and moves the robotic arm servos smoothly.

## Team
Developed by a 4-member engineering and education team in Almaty, Kazakhstan.
