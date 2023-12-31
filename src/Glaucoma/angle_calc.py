import tracker
import cv2
import math

# Use must fan out right hand in the setting now, but we can modify it later

# class AngleDisplay():
#     def __init__(self, coordinates):
#         if len(coordinates) > 1:
#             self.first = coordinates[0]
#             self.second = coordinates[1]
#         elif len(coordinates) == 1:
#             self.first = coordinates[0]

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

tracker = tracker.handTracker()


def calcCrd(crdList):
    idx = 0
    while idx != len(crdList):
        crd = crdList[idx]
        label = crd[0]
        if label == "Left":
            x2 = crd[1]
            y2 = crd[2]
        elif label == "Right":
            x1 = crd[1]
            y1 = crd[2]
        idx += 1
    return x1, y1, x2, y2


while True:
    success, img = cap.read()
    # mirror image
    img = cv2.flip(img, 1)
    img = tracker.handsFinder(img)
    coordinates = tracker.positionFinder(img)  # has coordinates

    try:
        x1, y1, x2, y2 = calcCrd(coordinates)

        # display coordinates
        cv2.putText(
            img,
            str(x1) + "," + str(y1),
            (x1, y1 + 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )
        cv2.putText(
            img,
            str(x2) + "," + str(y2),
            (x2, y2 + 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )
        # Draw line
        cv2.line(img, (x1, y1), (x2, img.shape[0]), (255, 255, 255), 5, cv2.FILLED)
        # Draw line and angle, depending on handedness
        cv2.line(img, (x2, y2), (x2, img.shape[0]), (255, 255, 255), 5, cv2.FILLED)

        print(img.shape[1])


        x1 = float(x1)
        x2 = float(x2)
        y1 = float(y1)
        y2 = float(y2)

        del_x = x1-x2
        del_y = img.shape[0] - y1

        try:
            angle = int(math.atan(del_x / del_y) * 180 / math.pi)
        except ZeroDivisionError:
            angle = None
        cv2.putText(
            img,
            str(angle),
            (int(x1) + 50, int((y2 + y1) / 2)),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

    except UnboundLocalError:
        print("Two hands need to be detected!")

    cv2.imshow("Hands", img)
    cv2.waitKey(1)
