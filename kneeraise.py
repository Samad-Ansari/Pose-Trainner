import cv2
import mediapipe as mp
import numpy as np
import winsound
 
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_leftleg_leftangle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 

def calculate_rightleg_rightangle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 

def rightlegboard(image, rightcounter, rightstage):

    cv2.rectangle(image, (420,0), (640,80), (245,117,16), -1)  # RIGHT RECTANGLE
    
    # # Rep data
    cv2.putText(image, 'RIGHT LEG REPS', (430,18), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
    cv2.putText(image, str(rightcounter), 
                (570,20), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2, cv2.LINE_AA)
    
    # # Stage data
    cv2.putText(image, 'RIGHT LEG STAGE', (430,60), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
    cv2.putText(image, rightstage, 
                (570,60), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2, cv2.LINE_AA)
  
def leftlegboard(image, leftcounter, leftstage):

    cv2.rectangle(image, (0,0), (220,80), (245,117,16), -1)  # LEFT RECTANGLE
    
    # Rep data
    cv2.putText(image, 'LEFT LEG REPS', (10,18), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
    cv2.putText(image, str(leftcounter), 
                (150,20), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2, cv2.LINE_AA)
    
    # Stage data
    cv2.putText(image, 'LEFT LEG STAGE', (10,60), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
    cv2.putText(image, leftstage, 
                (150,60), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2, cv2.LINE_AA)
    



    
def kneeraise():

    cap = cv2.VideoCapture(0)

    leftcounter = 0 
    leftstage = None

    rightcounter = 0 
    rightstage = None

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        
            # Make detection
            results = pose.process(image)
            correct_position = False
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark

# LEFT LEG COORDINATE
                righthip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x*640,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y*480]
                rightknee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x*640,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y*480]
                rightankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x*640,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y*480]
             
# RIGHT LEG COORDINATE
                lefthip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x*640,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y*480]
                leftknee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x*640,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y*480]
                leftankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x*640,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y*480]
        
                leftangle = calculate_leftleg_leftangle(lefthip, leftknee, leftankle)
                if leftangle > 170:
                    leftstage = "up"
                if leftangle < 95 and leftangle > 80 and leftstage =='up':
                    leftstage="down"
                    leftcounter +=1
     

                rightangle = calculate_rightleg_rightangle(righthip, rightknee, rightankle)
            
                if rightangle > 170:
                    rightstage = "up"
                if rightangle < 95 and rightangle > 80 and rightstage =='up':
                    rightstage="down"
                    rightcounter +=1
                    
                
            except:
                pass

# LEFT LEG BOARD
            
            leftlegboard(image, leftcounter, leftstage)

# RIGHT LEG BOARD

            rightlegboard(image, rightcounter, rightstage)

            
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    ) 


            
            cv2.imshow('Pose Trainner - Standing Knee Raise (press q to exit)', image)
            
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

