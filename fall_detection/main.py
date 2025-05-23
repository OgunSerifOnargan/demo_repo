import cv2
import numpy as np
from ultralytics import YOLO
import torch

# Model yolunu buraya gireceksiniz
MODEL_PATH = "/Users/onarganogun/Downloads/best.pt"  # Model dosya yolunu değiştirdim

# MPS cihazının kullanılabilirliğini kontrol et
device = 'mps' if torch.backends.mps.is_available() else 'cpu'
print(f"Kullanılan cihaz: {device}")

# Kamerayı başlat
cap = cv2.VideoCapture("rtsp://admin:endurans2024.@192.168.0.162:554/Streaming/channels/1?tcp")


# Modeli yükle ve MPS cihazına taşı
model = YOLO(MODEL_PATH)
model.to(device)  # Modeli MPS veya CPU'ya taşı

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Kamera görüntüsü alınamadı!")
        break

    # Model ile tahmin yap
    results = model(frame, device=device)  # Tahmini belirtilen cihazda yap

    # Tespit sonuçlarını frame üzerine çiz
    annotated_frame = results[0].plot()  # YOLOv8'in plot fonksiyonu kutuları ve etiketleri çizer

    # Frame'i göster
    cv2.imshow('YOLO Detection', annotated_frame)

    # 'q' tuşuna basılırsa çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları serbest bırak
cap.release()
cv2.destroyAllWindows()