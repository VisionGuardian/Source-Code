import cv2
import mediapipe as mp
import numpy as np

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
  
  def positionFinder(self, img, draw=True):
     lmlist = []
     if self.results.multi_hand_landmarks:
        for idx, handedness in enumerate(self.results.multi_handedness):
            Hand = self.results.multi_hand_landmarks[idx]
            for id, lm in enumerate(Hand.landmark):
                h, w, c = img.shape
                if id == 8:
                    cx, cy, cz = int(lm.x*w), int(lm.y*h), int(1/lm.z)
                    lmlist.append([handedness.classification[0].label, cx, cy, cz])
                    if draw:
                            # Blue
                            cv2.circle(img, (cx, cy), 10, (194, 67, 25), cv2.FILLED)

     return lmlist
  

def worldFinder(self, img, draw=True):
    lmlist = []
    # pseudo camera internals
    h, w, c = img.shape
    focal_length = w
    center = (w/2, h/2)
    camera_matrix = np.array(
                            [[focal_length, 0, center[0]],
                            [0, focal_length, center[1]],
                            [0, 0, 1]], dtype="double"
                            )
    distortion = np.zeros

    transformation = np.eye(4)

    return lmlist