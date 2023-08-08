import tracker
import cv2
import math

class AngleDisplay():
    def __init__(self, coordinates):
        # Case 1: 2 fingers detected
        # Case 2: 1 finger
        # Using elif to not have problem w/ 0 finger
        if len(coordinates) > 1:
            self.first = coordinates[0]
            self.second = coordinates[1]
        elif len(coordinates) == 1:
            self.first = coordinates[0]

    # def angleCalc(self, img, coordinates):
    #     cv.Put

cap = cv2.VideoCapture(0)
tracker = tracker.handTracker()

while True:
    success, img = cap.read()
    img = tracker.handsFinder(img)
    coordinates = tracker.positionFinder(img)    # has coordinates

    x1, y1, x2, y2 = 0, 0, 0, 0

    # assign coordinates
    if len(coordinates) > 1:
        x1 = coordinates[0][1]
        y1 = coordinates[0][2]
        x2 = coordinates[1][1]
        y2 = coordinates[1][2]
        cv2.putText(img, str(x2)+','+str(y2), (x2, y2+20), cv2.FONT_HERSHEY_SIMPLEX, 255,
                    (255,0,0))
    elif len(coordinates) == 1:
        x1 = coordinates[0][1]
        x2 = coordinates[0][2]
    
    cv2.putText(img, str(x1)+','+str(y1), (x1, y1+20), cv2.FONT_HERSHEY_SIMPLEX, 255,
                (255,0,0))
    # Draw line
    cv2.line(img, (x1,y1), (x2,y2), (255,255,255), 5, cv2.FILLED)

    cv2.imshow("Hands", img)
    cv2.waitKey(1)