import cv2
import numpy as np
import glob

# Chessboard boyutu (iç köşe sayısı)
CHESSBOARD_SIZE = (9,6)

# 3D noktaları hazırla (0,0,0) ... (8,5,0)
objp = np.zeros((CHESSBOARD_SIZE[0]*CHESSBOARD_SIZE[1],3), np.float32)
objp[:,:2] = np.mgrid[0:CHESSBOARD_SIZE[0],0:CHESSBOARD_SIZE[1]].T.reshape(-1,2)

objpoints = [] # 3D noktalar
imgpoints = [] # 2D köşeler

images = glob.glob('calib_images/*.jpg')  # kalibrasyon fotolarının klasörü
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, CHESSBOARD_SIZE, None)
    if ret:
        objpoints.append(objp)
        imgpoints.append(corners)
        cv2.drawChessboardCorners(img, CHESSBOARD_SIZE, corners, ret)
        cv2.imshow('img', img)
        cv2.waitKey(100)
cv2.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
print("Kamera matrisi:\n", mtx)
print("Distorsiyon katsayıları:\n", dist)
