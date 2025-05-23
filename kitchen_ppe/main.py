from ultralytics import YOLO
import cv2

# Modeli yükle
model_path = "/Users/onarganogun/Downloads/best-2.pt"
model = YOLO(model_path)

# İnference alacağımız görüntü
image_path = "kitchen_ppe/images/ChatGPT Image May 21, 2025 at 11_49_39 AM.png"
image = cv2.imread(image_path)

# İnference yap (conf=0.25 ile)
results = model.predict(source=image, conf=0.25)[0]

# Sonuçları orijinal görsel üzerinde çiz
annotated_frame = results.plot()

# Görseli göster
cv2.imshow("Inference Result", annotated_frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

