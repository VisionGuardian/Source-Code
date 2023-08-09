import cv2
import mediapipe as mp
import time
import platform

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
cTime = 0
pTime = 0

OS = platform.system()
if OS == 'Windows':
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
elif OS == 'Linux':
    cap = cv2.VideoCapture(-1, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Hand gesture detection algorithm
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            for id, lm in enumerate(handlms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)
                cv2.circle(img, (cx, cy), 15, (139, 0, 0), cv2.FILLED)
                mpDraw.draw_landmarks(img, handlms, mpHands.HAND_CONNECTIONS)

    # Time and FPS Calculation
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(
        img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (139, 0, 0), 3
    )

    cv2.imshow("Image", img)
    cv2.waitKey(1)

    if cv2.waitKey(1) & 0xFF == ord("q"):  # quit when 'q' is pressed
        cap.release()
        break
