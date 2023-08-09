import cv2
import mediapipe as mp


class poseTracker:
    def __init__(self):
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose()
        self.mpDraw = mp.solutions.drawing_utils
        # self.mpDrawingStyle = mp.solutions.drawing_styles

    '''
    Finds edge of the arms and torso.
    Marks (edge of) leftArm, rightArm, leftTorso, rightTorso
    '''
    def ptsFinder(self, img, draw=False):
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        img.flags.writeable = False
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(img)

        # Draw the pose annotation on the image.   
        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        self.results = self.pose.process(img)

        if draw:
            if self.results.pose_landmarks:
                self.mpDraw.draw_landmarks(
                    img,
                    self.results.pose_landmarks,
                    self.mpPose.POSE_CONNECTIONS
                )
        return img

    def positionFinder(self, img, draw=True):
        lmlist = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # In order: right wrist, left wrist, right shoulder, left shoulder
                if id==15 or id==16 or id==11 or id==12:
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    lmlist.append([id, cx, cy])
                    if draw:
                        cv2.circle(img, (cx, cy), 10, (194, 67, 25), cv2.FILLED)
        return lmlist