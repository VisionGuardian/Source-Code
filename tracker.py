import tracker
import cv2
import math

class Target:
    def __init__(self):
        self.capture = cv2.VideoCapture(0)
        cv2.namedWindow("Target", 1)
        cv2.namedWindow("Threshold1", 1)
        cv2.namedWindow("Threshold2", 1)
        cv2.namedWindow("hsv", 1)

cap = cv2.VideoCapture(0)
tracker = tracker.handTracker()

while True:
    success, img = cap.read()
    img = tracker.handsFinder(img)
    lmlist = tracker.positionFinder(img)
    print(type(lmlist))
    cv2.imshow("Hands", img)
    cv2.waitKey(1)