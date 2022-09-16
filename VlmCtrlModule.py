import cv2
import time
import numpy as np
import handTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class VlmCtrl():
    def Vlm(self):
        ##########################################
        wCam, hCam = 640, 480
        ##########################################

        cap = cv2.VideoCapture(0)
        cap.set(3, wCam)
        cap.set(4, hCam)
        pTime = 0

        detector = htm.handDetector(detectionCon=0.7)

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        # volume.GetMute()
        # volume.GetMasterVolumeLevel()
        volRange = volume.GetVolumeRange()
        # print(volume.GetVolumeRange())
        minVol = volRange[0]
        maxVol = volRange[1]
        vol = 0
        volBar = 400

        while True:
            success, img = cap.read()
            img = detector.findHands(img)
            lmList = detector.findPosition(img, draw=False)
            if len(lmList) != 0:
                # print(lmList[4], lmList[8])

                x1, y1 = lmList[4][1], lmList[4][2]
                x2, y2 = lmList[8][1], lmList[8][2]
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                cv2.circle(img, (x1, y1), 8, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 8, (255, 0, 255), cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

                # length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                length = math.hypot(x2 - x1, y2 - y1)
                # print(length)

                # hand range 50 - 200
                # volum range -96 - 0

                vol = np.interp(length, [50, 200], [minVol, maxVol])
                volBar = np.interp(length, [50, 200], [400, 150])

                # print(length, vol)
                volume.SetMasterVolumeLevel(vol, None)

                if length < 50:
                    cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)

                if length > 150:
                    cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

                x3, y3 = lmList[20][1], lmList[20][2]
                cv2.line(img, (x1, y1), (x3, y3), (255, 0, 255), 3)
                length1 = math.hypot(x3 - x1, y3 - y1)
                # print(length1)
                if length1 < 15:
                    break

            cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 5)
            cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)

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
    object = VlmCtrl()
    object.Vlm()

if __name__ == "__main__":
    main()