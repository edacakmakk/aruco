import cv2

for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Kamera bulundu: index {i}")
        cap.release()

# Bulduğun indeksi yaz:
cap = cv2.VideoCapture(1)  # 0 veya 1 olabilir
while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow("Camera Test", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC ile çık
        break

cap.release()
cv2.destroyAllWindows()
