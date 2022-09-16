import cv2
import handTrackingModule as htm
import math
import time
import pywifi
from pywifi import const

class WifiCtrl():
    def Wifi(self):
        #############################################################
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]

        iface.disconnect()
        time.sleep(1)
        assert iface.status() in \
               [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

        wifiId = pywifi.Profile()
        wifiId.ssid = 'Ridhim'
        wifiId.akm.append(const.AKM_TYPE_WPA2PSK)
        wifiId.auth = const.AUTH_ALG_OPEN
        wifiId.key = 'abcde'
        wifiId.cipher = const.CIPHER_TYPE_CCMP
       

        temp = iface.add_network_profile(wifiId)
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
            if len(lmList) != 0:
                # print(lmList[4], lmList[8])

                x1, y1 = lmList[4][1], lmList[4][2]
                x2, y2 = lmList[8][1], lmList[8][2]
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                length1 = math.hypot(x2 - x1, y2 - y1)
                if length1 < 20:
                    iface.connect(temp)
                    time.sleep(1)
                    assert iface.status() == const.IFACE_CONNECTED

                x3, y3 = lmList[20][1], lmList[20][2]
                cv2.line(img, (x1, y1), (x3, y3), (255, 0, 255), 3)
                length2 = math.hypot(x3 - x1, y3 - y1)
                # print(length1)
                if length2 < 20:
                    break

                x4, y4 = lmList[16][1], lmList[16][2]
                cv2.line(img, (x1, y1), (x4, y4), (255, 0, 255), 3)
                length3 = math.hypot(x4 - x1, y4 - y1)
                if length3 < 20:
                    iface.disconnect()
                    time.sleep(1)
                    assert iface.status() in \
                           [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

            cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                        1, (255, 0, 0), 3)

            cv2.imshow("Img", img)
            cv2.waitKey(1)

        cap.release()
        cv2.destroyAllWindows()

def main():
    object = WifiCtrl()
    object.Wifi()

if __name__ == "__main__":
    main()
