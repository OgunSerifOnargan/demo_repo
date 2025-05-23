import cv2
import numpy as np
import time
from coord_getter import get_coords

# RTSP akışını başlat
cap = cv2.VideoCapture("rtsp://admin:endurans2024.@192.168.0.162:554/Streaming/channels/1?tcp")

# ROI alanını al
lines = get_coords("rtsp://admin:endurans2024.@192.168.0.162:554/Streaming/channels/1?tcp", lineCounter=True)
roi_corners = [lines[0][0], lines[0][1], lines[1][0], lines[1][1]]

# ROI koordinatlarını hesapla
pts = np.array(roi_corners)
x, y = np.min(pts[:, 0]), np.min(pts[:, 1])
w = np.max(pts[:, 0]) - x
h = np.max(pts[:, 1]) - y
ROI = (x, y, w, h)

# Ortalama frame ve ayarlar
avg_frame = None
alpha = 0.01
STATIC_THRESHOLD = 30
PIXEL_COUNT_THRESHOLD = 1000
ALARM_TIME = 60

# Alarm zamanlayıcı
static_start_time = None
alarm_triggered = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    roi = frame[ROI[1]:ROI[1]+ROI[3], ROI[0]:ROI[0]+ROI[2]]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (15, 15), 0)

    if avg_frame is None:
        avg_frame = gray.astype("float")
        continue

    cv2.accumulateWeighted(gray, avg_frame, alpha)
    background = cv2.convertScaleAbs(avg_frame)
    diff = cv2.absdiff(background, gray)
    _, thresh = cv2.threshold(diff, STATIC_THRESHOLD, 255, cv2.THRESH_BINARY)
    thresh = cv2.dilate(thresh, None, iterations=2)

    changed_pixels = cv2.countNonZero(thresh)
    if changed_pixels < 50:
        alpha = 0.01
    else:
        alpha = 0.00001

    # Alarm kontrolü
    if changed_pixels > PIXEL_COUNT_THRESHOLD:
        if static_start_time is None:
            static_start_time = time.time()
        elif time.time() - static_start_time > ALARM_TIME and not alarm_triggered:
            print("⚠️ Alarm: Eşya bırakılmış olabilir!")
            cv2.imwrite("left_object.jpg", frame)
            alarm_triggered = True
    else:
        static_start_time = None
        alarm_triggered = False

    # Bounding box çizimi
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) < 500:
            continue
        x_box, y_box, w_box, h_box = cv2.boundingRect(cnt)
        cv2.rectangle(frame,
                      (x_box + ROI[0], y_box + ROI[1]),
                      (x_box + ROI[0] + w_box, y_box + ROI[1] + h_box),
                      (0, 0, 255), 2)

    # Görüntüleme
    cv2.imshow("ROI", roi)
    cv2.imshow("Fark", thresh)
    cv2.imshow("Main Frame with BBox", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
