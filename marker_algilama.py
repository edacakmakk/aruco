import cv2
from cv2 import aruco

cap = cv2.VideoCapture(1)
DICT = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
params = aruco.DetectorParameters()
detector = aruco.ArucoDetector(DICT, params)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    corners, ids, _ = detector.detectMarkers(frame)
    if ids is not None:
        aruco.drawDetectedMarkers(frame, corners, ids)
    cv2.imshow("Aruco Detection", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
