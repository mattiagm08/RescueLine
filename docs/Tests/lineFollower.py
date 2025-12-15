import cv2
import time
import numpy as np
from PID import PIDController

CAM_WIDTH = 640
CAM_HEIGHT = 480
ROI_HEIGHT_PERC = 0.20
VELOCITA_BASE = 100

KP = 0.4
KI = 0.001
KD = 2.0
CENTER_X = CAM_WIDTH // 2

pid = PIDController(Kp=KP, Ki=KI, Kd=KD, setpoint=CENTER_X, outputLimits=(-100, 100))

def setMotorSpeeds(leftSpeed, rightSpeed):
    leftSpeed = int(np.clip(leftSpeed, 0, 255))
    rightSpeed = int(np.clip(rightSpeed, 0, 255))
    pass

def mainLoop():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)
    
    if not cap.isOpened():
        print("Errore: Impossibile aprire la telecamera.")
        return

    while True:
        currentTime = time.time()
        
        ret, frame = cap.read()
        if not ret:
            print("Errore: Impossibile leggere il frame.")
            break

        roiYStart = int(CAM_HEIGHT * (1 - ROI_HEIGHT_PERC))
        roiFrame = frame[roiYStart:CAM_HEIGHT, 0:CAM_WIDTH]

        gray = cv2.cvtColor(roiFrame, cv2.COLOR_BGR2GRAY)
        _, threshold = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY_INV) 

        M = cv2.moments(threshold)
        
        lineCenterX = CENTER_X
        
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            lineCenterX = cx
            
        correction = pid.compute(lineCenterX, currentTime)

        motorSpeedLeft = VELOCITA_BASE - correction
        motorSpeedRight = VELOCITA_BASE + correction

        setMotorSpeeds(motorSpeedLeft, motorSpeedRight)

        cv2.circle(roiFrame, (lineCenterX, int(CAM_HEIGHT * ROI_HEIGHT_PERC / 2)), 5, (0, 0, 255), -1)
        cv2.circle(roiFrame, (CENTER_X, int(CAM_HEIGHT * ROI_HEIGHT_PERC / 2)), 5, (255, 0, 0), -1)
        
        cv2.imshow("Vision Line Follower - Threshold", threshold)
        cv2.imshow("Vision Line Follower - ROI", roiFrame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    mainLoop()