import cv2
import mediapipe as mp
import numpy as np
import winsound
 
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_rightleg_angle(rightknee, righthip):
    a = np.array(rightknee)
    b = np.array(righthip)
    c = [righthip[0], 0.9]
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = radians*180.0/np.pi
    if(angle < -10 or angle > 0):
        return True
    else:
        return False
    
def calculate_leftleg_angle(leftknee, lefthip):
    a = np.array(leftknee)
    b = np.array(lefthip)
    c = [lefthip[0], 0.9]
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = radians*180.0/np.pi
    if(angle > 10 or angle < 0):
        return True
    else:
        return False

def calculate_horizonshoulder_angle(leftshoulder, rightshoulder):
    a = np.array(leftshoulder)
    b = np.array(rightshoulder)
    c = [leftshoulder[0]+10, leftshoulder[1]]

    radians = np.arctan2(c[1]-a[1], c[0]-a[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = radians*180.0/np.pi
    if(angle > 10 or angle < -10):
        return True
    else:
        return False
    

def calculate_leftelbow_angle(leftshoulder, leftelbow):
    a = np.array(leftshoulder)
    b = np.array(leftelbow)
    c = [leftshoulder[1], leftshoulder[1]+10]

    radians = np.arctan2(c[1]-a[1], c[0]-a[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = radians*180.0/np.pi
    if(angle > 290 or angle < 270):
        return True
    else:
        return False
    

def calculate_rightelbow_angle(rightshoulder, rightelbow):
    a = np.array(rightshoulder)
    b = np.array(rightelbow)
    c = [rightshoulder[1], rightshoulder[1]+10]

    radians = np.arctan2(c[1]-a[1], c[0]-a[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = radians*180.0/np.pi
    if(angle > 265 or angle < 245):
        return True
    else:
        return False

def calculate_leftarm_leftangle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 

def calculate_rightarm_rightangle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 

def rightarmboard(image, rightcounter, rightstage):

    cv2.rectangle(image, (420,0), (640,80), (245,117,16), -1)  # RIGHT RECTANGLE
    
    # # Rep data
    cv2.putText(image, 'RIGHT ARM REPS', (430,18), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
    cv2.putText(image, str(rightcounter), 
                (570,20), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2, cv2.LINE_AA)
    
    # # Stage data
    cv2.putText(image, 'RIGHT ARM STAGE', (430,60), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
    cv2.putText(image, rightstage, 
                (570,60), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2, cv2.LINE_AA)
  
def leftarmboard(image, leftcounter, leftstage):

    cv2.rectangle(image, (0,0), (220,80), (245,117,16), -1)  # LEFT RECTANGLE
    
    # Rep data
    cv2.putText(image, 'LEFT ARM REPS', (10,18), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
    cv2.putText(image, str(leftcounter), 
                (150,20), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2, cv2.LINE_AA)
    
    # Stage data
    cv2.putText(image, 'LEFT ARM STAGE', (10,60), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
    cv2.putText(image, leftstage, 
                (150,60), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2, cv2.LINE_AA)
    


    
def bicepscurl():

    cap = cv2.VideoCapture(0)

    leftcounter = 0 
    leftstage = None
  
    rightcounter = 0 
    rightstage = None

    ## Setup mediapipe instance
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

# HIP
                lefthip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                righthip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
             
# KNEE
                leftknee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                rightknee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            
# SHOULDER
                
                leftshoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * 640, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y *480]
                rightshoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * 640, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * 480]
              
# ELBOW

                leftelbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * 640, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y *480]
                rightelbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x * 640, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y *480]

# WRIST
                leftwrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x*640,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y*480]
                rightwrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x*640,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y*480]
               
                if calculate_leftelbow_angle(leftshoulder, leftelbow):
                    winsound.Beep(2500, 80)
                    cv2.rectangle(image, (0,400), (180,450), (245,117,16), -1)
                    cv2.putText(image, "ADJUST LEFT ELBOW", (20,430), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
                elif calculate_rightelbow_angle(rightshoulder, rightelbow):
                    winsound.Beep(2500, 80)
                    cv2.rectangle(image, (0,400), (180,450), (245,117,16), -1)
                    cv2.putText(image, "ADJUST RIGHT ELBOW", (20,430), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
                elif calculate_horizonshoulder_angle(leftshoulder, rightshoulder):
                    winsound.Beep(2500, 80)
                    cv2.rectangle(image, (0,400), (180,450), (245,117,16), -1)
                    cv2.putText(image, "ADJUST BOTH SHOULDER", (20,430), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
                elif calculate_leftleg_angle(leftknee, lefthip):
                    winsound.Beep(2500, 80)
                    cv2.rectangle(image, (0,400), (180,450), (245,117,16), -1)
                    cv2.putText(image, "ADJUST LEFT LEG", (20,430), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
                elif calculate_rightleg_angle(rightknee, righthip):
                    winsound.Beep(2500, 80)
                    cv2.rectangle(image, (0,400), (180,450), (245,117,16), -1)
                    cv2.putText(image, "ADJUST RIGHT LEG", (20,430), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
                else:
                    correct_position = True

                # Calculate angle
                # Curl counter logic
                if correct_position:
                    leftangle = calculate_leftarm_leftangle(leftshoulder, leftelbow, leftwrist)
                    if leftangle > 150:
                        leftstage = "down"
                    if leftangle < 30 and leftstage =='down':
                        leftstage="up"
                        leftcounter +=1
         
                    rightangle = calculate_rightarm_rightangle(rightshoulder, rightelbow, rightwrist)
                    # Curl counter logic
                    if rightangle > 160:
                        rightstage = "down"
                    if rightangle < 30 and rightstage =='down':
                        rightstage="up"
                        rightcounter +=1
                        
            except:
                pass

# LEFT ARM 
            
            leftarmboard(image, leftcounter, leftstage)

# RIGHT ARM 

            rightarmboard(image, rightcounter, rightstage)

            
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    ) 


            
            cv2.imshow('Pose Trainner - Biceps Curl (press q to exit)', image)
            
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

