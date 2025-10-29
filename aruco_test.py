import cv2
import cv2.aruco as aruco

# Kamera açma
cap = cv2.VideoCapture(0)

# ArUco sözlüğü oluşturma
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)  # Yeni yöntem
parameters = aruco.DetectorParameters()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Marker tespiti
    corners, ids, rejected = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)

    # Markerleri çizdirme
    if ids is not None:
        aruco.drawDetectedMarkers(frame, corners, ids)

    cv2.imshow('frame', frame)

    # Çıkış için 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
