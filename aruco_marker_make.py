import cv2
import cv2.aruco as aruco

# ArUco sözlüğü seç (6x6 boyutunda, 250 marker'lık set)
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)

# Marker parametreleri
marker_id = 8        # 0 numaralı marker
marker_size = 200    # piksel boyutu

# Marker oluşturma
marker_image = aruco.generateImageMarker(aruco_dict, marker_id, marker_size)

# Kaydetme
cv2.imwrite("aruco_marker.png", marker_image)
print("ArUco marker kaydedildi: aruco_marker.png")
