from flask import Flask, Response
import cv2

app = Flask(__name__)
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  # /dev/video0
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

def generate():
    while True:
        ok, frame = cap.read()
        if not ok:
            continue
        # İstersen burada ArUco tespiti ekleyebilirsin
        _, buffer = cv2.imencode(".jpg", frame)
        yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")

@app.route("/")
def video_feed():
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
