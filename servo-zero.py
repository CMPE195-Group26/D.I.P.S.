import sys
sys.path.append('./')
from servo import Servo
from time import sleep

PAN_SERVO_PIN = 12
TILT_SERVO_PIN = 13

panServo = Servo(PAN_SERVO_PIN)
tiltServo = Servo(TILT_SERVO_PIN)

while True:
    panServo.set_angle(0)
    tiltServo.set_angle(0)
    sleep(2)