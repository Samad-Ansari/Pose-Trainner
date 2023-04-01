import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_leftleg_angle(lefthip,leftknee,leftankle):
    lefthip = np.array(lefthip) # First
    leftknee = np.array(leftknee) # Mid
    leftankle = np.array(leftankle) # End
    
    radians = np.arctan2(leftankle[1]-leftknee[1], leftankle[0]-leftknee[0]) - np.arctan2(lefthip[1]-leftknee[1], lefthip[0]-leftknee[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle >180.0:
        angle = 360-angle
        
    return angle 


def calculate_rightleg_angle(righthip,rightknee,rightankle):
    righthip = np.array(righthip) # First
    rightknee = np.array(rightknee) # Mid
    rightankle = np.array(rightankle) # End
    radians = np.arctan2(rightankle[1]-rightknee[1], rightankle[0]-rightknee[0]) - np.arctan2(righthip[1]-rightknee[1], righthip[0]-rightknee[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle >180.0:
        angle = 360-angle
    return angle 

def calculate_ankle_distance(leftankle, rightankle, image):
    leftankle = np.array(leftankle)
    rightankle = np.array(rightankle)
    sqrs = (leftankle[1] - rightankle[1])**2 + (leftankle[0] - rightankle[0])**2
    distance = np.sqrt(sqrs)


    cv2.putText(image, str(distance), (100,100), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                
    if distance > 120 or distance < 90:
        winsound.Beep(2500, 80)
        cv2.rectangle(image, (0,400), (220,450), (245,117,16), -1)
        cv2.putText(image, "ADJUST ANKLE DISTANCE", (20,430), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)


def squats():

    cap = cv2.VideoCapture(0)

    counter = 0 
    stage = None

    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        
            # Make detection
            results = pose.process(image)
        
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates
                lefthip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x*640,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y*480]
                leftknee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x*640,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y*480]
                leftankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x*640,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y*480]

                righthip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x*640,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y*480]
                rightknee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x*640,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y*480]
                rightankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x*640,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y*480]
              
                # Calculate angle
                leftangle = calculate_leftleg_angle(lefthip, leftknee, leftankle)
                rightangle = calculate_rightleg_angle(righthip, rightknee, rightankle)
                
                calculate_ankle_distance(leftankle, rightankle, image)
                
                if rightangle > 150 and leftangle > 150:
                    stage = "up"
                if leftangle < 120 and rightangle < 120 and stage =='up':
                    stage="down"
                    counter +=1      
            except:
                pass
            
            # # Render curl counter
            # # Setup status box
               
            cv2.rectangle(image, (0,0), (220,80), (245,117,16), -1)  # LEFT RECTANGLE
            
            # Rep data
            cv2.putText(image, 'REPS', (10,18), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter), 
                        (150,20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2, cv2.LINE_AA)
            
            # Stage data
            cv2.putText(image, 'STAGE', (10,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage, 
                        (150,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2, cv2.LINE_AA)
            


     
            
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )               
            
            cv2.imshow('Pose Trainner - Squats (press q to exit)', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
