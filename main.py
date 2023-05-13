#toptechboy helped with understanding the fundamentals of this project through his youtube series
import cv2
from picamera2 import Picamera2
import time
import numpy as np
from servo import Servo


picam2 = Picamera2()

pan = Servo(pin=12)
tilt = Servo(pin=13)
panAngle = 0
tiltAngle = 0
pan.set_angle(panAngle)
tilt.set_angle(tiltAngle)

dispW = 960
dispH = 540
picam2.preview_configuration.main.size = (dispW, dispH)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.controls.FrameRate = 30
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

fps = 0
pos = (30, 60)
textFont = cv2.FONT_HERSHEY_COMPLEX
textHeight = 1.5
textWeight = 3
myColor = (0, 0, 255)

#Creating and Setting Trackbar Values


hueLow = 2


def trackbar1(val):
    global hueLow
    hueLow = val
    print('Hue Low', hueLow)


hueHigh = 19


def trackbar2(val):
    global hueHigh
    hueHigh = val
    print('Hue High', hueHigh)


saturationLow = 112


def trackbar3(val):
    global saturationLow
    saturationLow = val
    print('Sat Low', saturationLow)


saturationHigh = 255


def trackbar4(val):
    global saturationHigh
    saturationHigh = val
    print('Sat High', saturationHigh)


valueLow = 147


def trackbar5(val):
    global valueLow
    valueLow = val
    print('Val Low', valueLow)


valueHigh = 255


def trackbar6(val):
    global valueHigh
    valueHigh = val
    print('Val High', valueHigh)


track = 0


def trackbar7(val):
    global track
    track = val
    print('Track Value', track)


showContour = 0


def trackbar8(val):
    global showContour
    showContour = val
    print('Show Contour', showContour)


cv2.namedWindow('Trackbars')

cv2.createTrackbar('Hue Low', 'myTracker', 10, 179, trackbar1)
cv2.createTrackbar('Hue High', 'myTracker', 20, 179, trackbar2)
cv2.createTrackbar('Sat Low', 'myTracker', 100, 255, trackbar3)
cv2.createTrackbar('Sat High', 'myTracker', 255, 255, trackbar4)
cv2.createTrackbar('Val Low', 'myTracker', 100, 255, trackbar5)
cv2.createTrackbar('Val High', 'myTracker', 255, 255, trackbar6)
cv2.createTrackbar('Train-0 Track-1', 'myTracker', 0, 1, trackbar7)
cv2.createTrackbar('No Contours-0 Show Contours-1', 'myTracker', 0, 1, trackbar8)

while True:
    tStart = time.time()
    frame = picam2.capture_array()
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.putText(frame, str(int(fps)) + ' FPS', pos, textFont, textHeight, myColor, textWeight)
    lowerBound = np.array([hueLow, saturationLow, valueLow])
    upperBound = np.array([hueHigh, saturationHigh, valueHigh])
    myMask = cv2.inRange(frameHSV, lowerBound, upperBound)
    myMaskSmall = cv2.resize(myMask, (int(dispW / 2), int(dispH / 2)))
    myObject = cv2.bitwise_and(frame, frame, mask=myMask)
    myObjectSmall = cv2.resize(myObject, (int(dispW / 2), int(dispH / 2)))

    contours, junk = cv2.findContours(myMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
        if showContour == 1:
            cv2.drawContours(frame, contours, -1, (255, 0, 0), 3)
        contour = contours[0]
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
        if track == 1:
            panError = (x + w / 2) - dispW / 2
            if panError > 35:
                panAngle = panAngle - (panError / 70)  # Lower numbers = higher sensitivity, default value = 70
                if panAngle < -90:
                    panAngle = -90
                pan.set_angle(panAngle)
            if panError < -35:
                panAngle = panAngle + (-panError / 70)
                if panAngle > 90:
                    panAngle = 90
                pan.set_angle(panAngle)
            tiltError = (y + h / 2) - dispH / 2
            if tiltError > 35:
                tiltAngle = tiltAngle - (tiltError / 70)
                if tiltAngle < -40:
                    tiltAngle = -40
                tilt.set_angle(tiltAngle)
            if tiltError < -35:
                tiltAngle = tiltAngle + (-tiltError / 70)
                if tiltAngle > 90:
                    tiltAngle = 90
                tilt.set_angle(tiltAngle)

    cv2.imshow('Camera', frame)
    cv2.imshow('My Object', myObjectSmall)
    if cv2.waitKey(1) == ord('q'):
        break
    tEnd = time.time()
    loopTime = tEnd - tStart
    fps = .9 * fps + .1 * (1 / loopTime)
cv2.destroyAllWindows()

