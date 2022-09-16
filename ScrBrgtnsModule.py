import cv2
import handTrackingModule as htm
import math
import time
import screen_brightness_control as sbc

class ScrBrgtns():
    def ScrBrgtns(self):
        #############################################################

        #############################################################

        wCam, hCam = 640, 480
        cap = cv2.VideoCapture(0)
        cap.set(3, wCam)
        cap.set(4, hCam)
        pTime = 0

        detector = htm.handDetector(detectionCon=0.7)

        while True:
            success, img = cap.read()
            img = detector.findHands(img)
            lmList = detector.findPosition(img, draw=False)
            x = 20
            # sbc.set_brightness(50)
            if len(lmList) != 0:

                x1, y1 = lmList[4][1], lmList[4][2]
                x2, y2 = lmList[8][1], lmList[8][2]
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                length1 = math.hypot(x2 - x1, y2 - y1)
                if length1 < 30:
                    sbc.set_brightness(x+20)

                x3, y3 = lmList[20][1], lmList[20][2]
                cv2.line(img, (x1, y1), (x3, y3), (255, 0, 255), 3)
                length2 = math.hypot(x3 - x1, y3 - y1)
                if length2 < 20:
                    break

                x4, y4 = lmList[16][1], lmList[16][2]
                cv2.line(img, (x1, y1), (x4, y4), (255, 0, 255), 3)
                length3 = math.hypot(x4 - x1, y4 - y1)
                if length3 < 30:
                    sbc.set_brightness(x-20)
                
                x5, y5 = lmList[12][1], lmList[12][2]
                cv2.line(img, (x1, y1,), (x5, y5), (255, 0, 255), 3)
                length4 = math.hypot(x5-x1, y5-y1)
                if length4 < 20:
                    sbc.set_brightness(50)

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

            cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                        1, (255, 0, 0), 3)

            cv2.imshow("Img", img)
            cv2.waitKey(1)

        # After the loop release the cap object
        cap.release()
        # Destroy all the windows
        cv2.destroyAllWindows()

def main():
    object = ScrBrgtns()
    object.ScrBrgtns()

if __name__ == "__main__":
    main()
