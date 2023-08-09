import pose
import cv2
import math
import time
import platform


def calcCrd(crdList):
    idx = 0
    while idx != len(crdList):
        crd = crdList[idx]
        id = crd[0]
        if id == 15:
            x_rarm = crd[1]
            y_rarm = crd[2]
        elif id == 16:
            x_larm = crd[1]
            y_larm = crd[2]
        elif id == 11:
            x_rsh = crd[1]
            y_rsh = crd[2]
        elif id == 12:
            x_lsh = crd[1]
            y_lsh = crd[2]
        idx += 1
    return x_rarm, y_rarm, x_larm, y_larm, x_rsh, y_rsh, x_lsh, y_lsh

# Does not have to be iterated
def calibration(cap):
    arm = 0.0
    torso = 0.0

    while arm == 0.0 and torso == 0.0:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        tracker = pose.poseTracker()
        coordinates = tracker.positionFinder(img)  # has coordinates  

        try:
            x_rarm, y_rarm, x_larm, y_larm, x_rsh, y_rsh, x_lsh, y_lsh = calcCrd(coordinates)

            # display coordinates
            cv2.putText(
                img,
                str(x_rarm) + "," + str(y_rarm),
                (x_rarm, y_rarm + 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )
            cv2.putText(
                img,
                str(x_larm) + "," + str(y_larm),
                (x_larm, y_larm + 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )
            cv2.putText(
                img,
                str(x_rsh) + "," + str(y_rsh),
                (x_rsh, y_rsh + 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )
            cv2.putText(
                img,
                str(x_lsh) + "," + str(y_lsh),
                (x_lsh, y_lsh + 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )

            # Aerial angle calculation        
            # Calculate when all points are pretty much parallel
            if abs(y_rarm - y_larm) < 3 and abs(y_rsh - y_rarm) < 5 and abs(y_lsh - y_larm) < 5:
                # 1. Arm Length -- average of two detected arm length
                arm = ((x_lsh - x_larm) + (x_rarm - x_rsh)) / 2
                # 2. Torso length
                torso = x_rsh - x_lsh
                break

            cv2.imshow("Calibration", img)
            cv2.waitKey(1)

        except UnboundLocalError:
            print("Upper body detection needed for calibration!")

    return arm, torso
    

OS = platform.system()
if OS == 'Windows':
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
elif OS == 'Linux':
    cap = cv2.VideoCapture(-1, cv2.CAP_DSHOW)
else:   # mac
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Get Values for arm and torso
arm, torso = calibration(cap)
print(arm, torso)

print("Start of procedure in 5 seconds")
time.sleep(5)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    tracker = pose.poseTracker()

    coordinates = tracker.positionFinder(img)  # has coordinates  
    try:
        x_rarm, y_rarm, x_larm, y_larm, x_rsh, y_rsh, x_lsh, y_lsh = calcCrd(coordinates)
    except UnboundLocalError:
        print("Four upper body points needed!")

    try:
        angle = int(math.asin((x_rarm - x_larm) / (arm + torso)**2) * 180 / math.pi)
    except ZeroDivisionError:
        angle = None

    print(angle)

    cv2.imshow("Angle Calc", img)
    cv2.waitKey(1)

    print(angle)