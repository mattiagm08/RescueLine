import cv2 as cv
import numpy as np
import time

def main():
    
    cam = cv.VideoCapture(0)

    while True:
        ret, frame = cam.read()

        if not ret:
            print("\nTentativo di cattura fallito.\n")
            break

        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        #RANGE VERDE HSV
        lowerGreen = np.array([40, 50, 50])
        upperGreen = np.array([80, 255, 255])

        #MASCHERA VERDE
        maskGreen = cv.inRange(hsv, lowerGreen, upperGreen)

        #RISULTATO
        resultGreen = cv.bitwise_and(frame, frame, mask=maskGreen)

        #DIVIDI IL FRAME IN DUE LATI DX E SX
        

        #CONTORNI VERDI
        contoursGreen, _ = cv.findContours(maskGreen, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        if contoursGreen:
            largestContourGreen = max(contoursGreen, key=cv.contourArea)
            if cv.contourArea(largestContourGreen) > 10000:  
                cv.drawContours(frame, [largestContourGreen], -1, (0, 255, 0), 3)
                print("Contorno verde rilevato.")
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

        cv.imshow("Frame", frame)
        cv.imshow("Rilevamento Verde", resultGreen)
        time.sleep(0.1)

if __name__ == "__main__":
    main()