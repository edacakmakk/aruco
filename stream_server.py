# stream_server.py  (Picamera2 + Flask + ArUco, OpenCV 4.10 uyumlu)
import time
import cv2
import numpy as np
from flask import Flask, Response
from picamera2 import Picamera2

picam2 = Picamera2()
config = picam2.create_video_configuration(
    main={"size": (640, 480), "format": "RGB888"},
    controls={"FrameRate": 200}
)
picam2.configure(config)
picam2.start()
time.sleep(0.5)



aruco = cv2.aruco
# prepare multiple dictionaries to try
dict_candidates = {
    "4x4_50": aruco.getPredefinedDictionary(aruco.DICT_4X4_50),
    "6x6_50": aruco.getPredefinedDictionary(aruco.DICT_6X6_50),
}
# default to one for detector creation (if using ArucoDetector)
dictionary = dict_candidates["6x6_50"]

# Create detector parameters in a way that works across OpenCV versions
parameters = None
if hasattr(aruco, "DetectorParameters_create"):
    try:
        parameters = aruco.DetectorParameters_create()
    except Exception:
        parameters = None

if parameters is None and hasattr(aruco, "DetectorParameters"):
    try:
        parameters = aruco.DetectorParameters()
    except Exception:
        parameters = None

# Create detector if available (OpenCV >= 4.7); otherwise we'll use detectMarkers()
detector = None
if hasattr(aruco, "ArucoDetector"):
    if parameters is not None:
        detector = aruco.ArucoDetector(dictionary, parameters)
    else:
        detector = aruco.ArucoDetector(dictionary)

app = Flask(__name__)

def gen():
    last_time = time.time()
    while True:
        fps = 1/(time.time()-last_time)
        print(f"  {1/(time.time()-last_time):.1f}           ", end="\r")
        last_time = time.time()

        frame = picam2.capture_array()
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        corners, ids = None, None
        # if ArucoDetector available you can create one per dictionary; simpler: try detectMarkers per dict
        for name, d in dict_candidates.items():
            if hasattr(aruco, "ArucoDetector"):
                # build a temporary detector for this dictionary
                det = aruco.ArucoDetector(d, parameters) if parameters is not None else aruco.ArucoDetector(d)
                c, i, _ = det.detectMarkers(frame_bgr)
            else:
                c, i, _ = aruco.detectMarkers(frame_bgr, d)

            if i is not None and len(i) > 0:
                corners, ids = c, i
                break

        if ids is not None and len(ids) > 0:
            aruco.drawDetectedMarkers(frame_bgr, corners, ids)

        cv2.putText(frame_bgr, f"ids: {0 if ids is None else len(ids)} fps: {fps:.1f}",
                    (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2, cv2.LINE_AA)

        ok, jpeg = cv2.imencode(".jpg", frame_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
        if not ok:
            continue
        yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n")

@app.route("/")
def index():
    return ('<html><body style="margin:0;background:#000;">'
            '<img src="/video" style="width:100vw;height:auto;display:block;"/>'
            '</body></html>')

@app.route("/video")
def video():
    return Response(gen(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
