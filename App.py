import cv2
import time
import handTrackingModule as htm
import math
########################################################################
import screen_brightness_control as sbc
########################################################################
import pywifi
from pywifi import const
########################################################################
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
########################################################################


class App():
   def ScrBrgtns(self):
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
         x = 40
         # sbc.set_brightness(50)
         if len(lmList) != 0:

            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            length1 = math.hypot(x2 - x1, y2 - y1)
            if length1 < 30:
               sbc.set_brightness(x + 20)

            x3, y3 = lmList[20][1], lmList[20][2]
            cv2.line(img, (x1, y1), (x3, y3), (255, 0, 255), 3)
            length2 = math.hypot(x3 - x1, y3 - y1)
            if length2 < 20:
               break

            x4, y4 = lmList[16][1], lmList[16][2]
            cv2.line(img, (x1, y1), (x4, y4), (255, 0, 255), 3)
            length3 = math.hypot(x4 - x1, y4 - y1)
            if length3 < 30:
               sbc.set_brightness(x - 20)

            x5, y5 = lmList[12][1], lmList[12][2]
            cv2.line(img, (x1, y1,), (x5, y5), (255, 0, 255), 3)
            length4 = math.hypot(x5 - x1, y5 - y1)
            if length4 < 20:
               sbc.set_brightness(50)

         cTime = time.time()
         fps = 1 / (cTime - pTime)
         pTime = cTime

         cv2.putText(img, "Brightness Control", (300, 50), cv2.FONT_HERSHEY_COMPLEX,
                     1, (255, 0, 0), 3)
         cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                     1, (255, 0, 0), 3)

         cv2.imshow("Img", img)
         cv2.waitKey(1)

   def Vlm(self):

      wCam, hCam = 640, 480
      cap = cv2.VideoCapture(0)
      cap.set(3, wCam)
      cap.set(4, hCam)
      pTime = 0

      detector = htm.handDetector(detectionCon=0.7)

      devices = AudioUtilities.GetSpeakers()
      interface = devices.Activate(
         IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
      volume = cast(interface, POINTER(IAudioEndpointVolume))
      volRange = volume.GetVolumeRange()
      minVol = volRange[0]
      maxVol = volRange[1]
      vol = 0
      volBar = 400

      while True:
         success, img = cap.read()
         img = detector.findHands(img)
         lmList = detector.findPosition(img, draw=False)
         if len(lmList) != 0:

            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            cv2.circle(img, (x1, y1), 8, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 8, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

            length = math.hypot(x2 - x1, y2 - y1)

            # hand range 50 - 200 # volum range -96 - 0

            vol = np.interp(length, [50, 200], [minVol, maxVol])
            volBar = np.interp(length, [50, 200], [400, 150])

            volume.SetMasterVolumeLevel(vol, None)

            if length < 50:
               cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)

            if length > 150:
               cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

            x3, y3 = lmList[20][1], lmList[20][2]
            cv2.line(img, (x1, y1), (x3, y3), (255, 0, 255), 3)
            length1 = math.hypot(x3 - x1, y3 - y1)
            if length1 < 15:
               self.menu()
               time.sleep(2)

         cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 5)
         cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)

         cTime = time.time()
         fps = 1 / (cTime - pTime)
         pTime = cTime

         cv2.putText(img, "Volume Control", (300, 50), cv2.FONT_HERSHEY_COMPLEX,
                     1, (255, 0, 0), 3)
         cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                     1, (255, 0, 0), 3)

         cv2.imshow("Img", img)
         cv2.waitKey(1)

   def Wifi(self):

      wifi = pywifi.PyWiFi()
      iface = wifi.interfaces()[0]

      iface.disconnect()
      time.sleep(1)
      assert iface.status() in \
             [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

      profile = pywifi.Profile()
      profile.ssid = 'Darsh'
      profile.auth = const.AUTH_ALG_OPEN
      profile.akm.append(const.AKM_TYPE_WPA2PSK)
      profile.cipher = const.CIPHER_TYPE_CCMP
      profile.key = None
      tmp_profile = iface.add_network_profile(profile)

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

            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            length1 = math.hypot(x2 - x1, y2 - y1)
            if length1 < 30:
               iface.connect(tmp_profile)
               time.sleep(1)
               assert iface.status() == const.IFACE_CONNECTED

            x3, y3 = lmList[20][1], lmList[20][2]
            cv2.line(img, (x1, y1), (x3, y3), (255, 0, 255), 3)
            length2 = math.hypot(x3 - x1, y3 - y1)
            if length2 < 20:
               self.menu()
               time.sleep(2)

            x4, y4 = lmList[16][1], lmList[16][2]
            cv2.line(img, (x1, y1), (x4, y4), (255, 0, 255), 3)
            length3 = math.hypot(x4 - x1, y4 - y1)
            if length3 < 30:
               iface.disconnect()
               time.sleep(1)
               assert iface.status() in \
                      [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

         cTime = time.time()
         fps = 1 / (cTime - pTime)
         pTime = cTime

         cv2.putText(img,"Wifi Control",(300, 50), cv2.FONT_HERSHEY_COMPLEX,
                     1, (255, 0, 0), 3)
         cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                     1, (255, 0, 0), 3)

         cv2.imshow("Img", img)
         cv2.waitKey(1)


   def menu(self):
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

         cTime = time.time()
         fps = 1 / (cTime - pTime)
         pTime = cTime

         if len(lmList) != 0:

            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            length1 = math.hypot(x2 - x1, y2 - y1)
            if length1 < 30:
               self.Vlm()

            x3, y3 = lmList[20][1], lmList[20][2]
            cv2.line(img, (x1, y1), (x3, y3), (255, 0, 255), 3)
            length2 = math.hypot(x3 - x1, y3 - y1)
            if length2 < 30:
               break

            x4, y4 = lmList[16][1], lmList[16][2]
            cv2.line(img, (x1, y1), (x4, y4), (255, 0, 255), 3)
            length3 = math.hypot(x4 - x1, y4 - y1)
            if length3 < 30:
               self.Wifi()

            x5, y5 = lmList[12][1], lmList[12][2]
            cv2.line(img, (x1, y1,), (x5, y5), (255, 0, 255), 3)
            length4 = math.hypot(x5 - x1, y5 - y1)
            if length4 < 20:
               self.ScrBrgtns()

         cv2.putText(img, "Menu",(300, 50), cv2.FONT_HERSHEY_COMPLEX,
                     1, (255, 0, 0), 3)
         cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                     1, (255, 0, 0), 3)

         cv2.imshow("Img", img)
         if cv2.waitKey(1) == ord('q'):
            break

def main():
   o = App()
   o.menu()

if __name__ == "__main__":
   main()




