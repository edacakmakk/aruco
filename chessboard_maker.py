import cv2
from cv2 import aruco

# 9x6 iç köşe -> 10x7 kare
squares_x, squares_y = 10, 7
square_length = 50  # px cinsinden
marker_length = 25  # opsiyonel

board = aruco.CharucoBoard((squares_x, squares_y),
                            square_length, marker_length,
                            aruco.getPredefinedDictionary(aruco.DICT_4X4_50))

img = board.generateImage((1000, 700))
cv2.imwrite("chessboard.png", img)
cv2.imshow("Board", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
