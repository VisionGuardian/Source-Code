import cv2
import mediapipe as mp

class handTracker():
  def __init__(self, mode=False, maxHands=2, detectionCon=0.5, modelComplexity=1, trackCon=0.5):
      self.mode = mode
      self.maxHands = maxHands
      self.detectionCon = detectionCon
      self.modelComplex = modelComplexity
      self.trackCon = trackCon
      self.mpHands = mp.solutions.hands
      self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex,
                                      self.detectionCon, self.trackCon)
      self.mpDraw = mp.solutions.drawing_utils

  def handsFinder(self, img, draw=True):
      imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
      self.results = self.hands.process(imgRGB)
      if self.results.multi_hand_landmarks:
         for handlms in self.results.multi_hand_landmarks:
            if draw:
               self.mpDraw.draw_landmarks(img, handlms, self.mpHands.HAND_CONNECTIONS)
      return img
  
  def positionFinder(self, img, handNo=0, draw=True):
     lmlist = []
     if self.results.multi_hand_landmarks:
        for handNo in range(len(self.results.multi_handedness)):
            Hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(Hand.landmark):
                h, w, c = img.shape
                if id == 8:
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    lmlist.append([handNo, cx, cy])
                    if draw:
                        if handNo == 0:
                            cv2.circle(img, (cx, cy), 10, (194, 67, 25), cv2.FILLED)
                        else:
                            cv2.circle(img, (cx, cy), 10, (25, 67, 194), cv2.FILLED)

     return lmlist