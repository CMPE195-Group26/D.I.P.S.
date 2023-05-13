# Detection of Incoming Projectile System (D.I.P.S.)


## Dependent Libraries
- Python 3 
- OpenCV
- Picamera2
- PiGPIO

## Hardware Requirements
- Raspberry Pi microcomputer
- 2 SG90 Servos/equivalent
- Raspberry Pi Camera/equivalent

## Instructions
1. Assuming Raspberry Pi has been set up and on the OS, open the terminal.
2. Ensure the following libraries have been installed (we will use pip to do this, assuming a version of Python 3 is already installed):
```
sudo apt install python3-pip
pip install pigpio
pip install picamera2
pip install numpy
pip install opencv-python
```
3. Download the project or via git clone and navigate to the project directory. 4 files should be present:
- main.py
- servo-zero.py
- servo.py
- README.md 

### Zero out Servos
To zero out the servos, run servo-zero.py. This sets the angles of the servos to 0 and can be ran after the main program has finished to re-center the camera's position.
```
python3 servo-zero.py
```

### Start Main Program
After setting the servo angles, Run the main program:
```
python3 main.py
```
3 Windows will pop up, consisting of the Trackbar Window, Mask Window, and the Camera Window. The Program will automatically start on **train** mode.
Train the program to lock onto your color by modifying the trackbar values. When the color is locked on, you can then set the system to **tracking** mode, and the camera will lock onto the largest object within the given HSV values.

To terminate the program, use a keyboard interrupt (like CTRL + C) or Stop in your IDE. Zero out the servos if desired.
