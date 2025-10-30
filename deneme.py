# ~9fps 4.7.0
import cv2
import time
from picamera2 import Picamera2

# pycam
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(
                            main={"format": 'BGR888', 'size': (320, 240)}, 
                            buffer_count=1))
picam2.start()

# aruco
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)
aruco_params = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

last_time = time.time()
while True:
    print(f"  {1/(time.time()-last_time):.1f}           ", end="\r")
    last_time = time.time()
        
    img = picam2.capture_array(wait=True)

    #aruco stuff
    corners, ids, rejected = detector.detectMarkers(img)
