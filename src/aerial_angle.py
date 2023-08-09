import pose
import cv2
import math
import time
import platform

OS = platform.system()
if OS == 'Windows':
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
elif OS == 'Linux':
    cap = cv2.VideoCapture(-1, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

tracker = pose.poseTracker()


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


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = tracker.ptsFinder(img)
    coordinates = tracker.positionFinder(img)  # has coordinates
    print(coordinates)

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

    except UnboundLocalError:
        print("Upper body detection needed for calibration!")

    cv2.imshow("Aerial Angle", img)
    cv2.waitKey(1)