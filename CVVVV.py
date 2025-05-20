import mediapipe as mp
import mediapipe as mp
print(mp.__version__)

import mediapipe as mp
print(mp.__version__)
import cv2
import mediapipe as mp
import numpy as np
import time
import warnings
warnings.filterwarnings("ignore")


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


cap = cv2.VideoCapture(0)


cap.set(3, 2000)
cap.set(4, 2000)


#previous time
ptime = 0
#current time
ctime = 0 


counter = 0
stage = None

def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180 / np.pi)

    if angle > 180:
        angle = 360 - angle

    return angle


with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(frame)

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        try:
            landmarks = result.pose_landmarks.landmark
            
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            angle = calculate_angle(shoulder, elbow, wrist)

            cv2.putText(frame, str(angle),
                        tuple(np.multiply(elbow, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            
              
            if angle > 160:
                stage = "Down"
                
            if angle < 45 and stage =="Down":
                stage="Up"
                counter +=1
                print(counter)

        except:
            pass

        cv2.rectangle(frame , (0,0) , (235,73) , (245,117,16),-1)
        
        cv2.putText(frame , "REPS",(15,12),
                   cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA)
        
        cv2.putText(frame , str(counter),(10,60),
                   cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,0),2,cv2.LINE_AA)
        
        cv2.putText(frame , "STAGE",(75,12),
                   cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA)
        
        cv2.putText(frame , stage,(80,60),
                   cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA)



        mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=4, circle_radius=4),
                                  mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=4, circle_radius=3))
        

        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        cv2.putText(frame, f"FPS: {int(fps)}", (10,120), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 255), 6)

        cv2.imshow("Frame", frame)

        if cv2.waitKey(10) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
