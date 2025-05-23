import cv2
import numpy as np

# 1 TL çapı mm cinsinden
TL_DIAMETER_MM = 26.15
CARROT_DENSITY_G_CM3 = 0.64

def find_circle_diameter_pixels(image_path):
    # Görüntüyü yükle
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    
    # Hough Circle Transform ile daire bulma
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=100,
                               param1=50, param2=30, minRadius=10, maxRadius=100)
    
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        # İlk bulduğu çemberi kullanacağız
        x, y, r = circles[0]
        diameter_pixels = 2 * r
        return diameter_pixels, img, (x,y,r)
    else:
        raise Exception("Madeni para bulunamadı!")

import cv2
import numpy as np

def measure_carrot_length_pixels(image_path):
    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        raise Exception("Image could not be loaded!")

    # Convert to HSV for color-based segmentation of the carrot
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define the color range for the carrot (orange)
    lower_orange = np.array([10, 100, 100])  # Lower bound for orange in HSV
    upper_orange = np.array([25, 255, 255])  # Upper bound for orange in HSV
    mask_carrot = cv2.inRange(hsv, lower_orange, upper_orange)

    # Convert to grayscale for additional processing
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    gray = cv2.GaussianBlur(gray, (15, 15), 0)

    # Use adaptive thresholding to handle uneven lighting
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )

    # Combine the color-based mask with the adaptive threshold for the carrot
    combined_mask = cv2.bitwise_or(mask_carrot, thresh)

    # Remove reflection by applying a range-based intensity filter
    # Adjust the range to include the carrot's intensity and exclude the reflection
    _, intensity_mask = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)  # Lowered to 30
    combined_mask = cv2.bitwise_and(combined_mask, intensity_mask)

    # Apply morphological operations to clean up the mask and disconnect reflection
    kernel = np.ones((5, 5), np.uint8)
    combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)  # Remove small noise
    combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel, iterations=2)  # Fill gaps

    # Find contours
    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise Exception("No contours found!")

    # Get the largest contour (assumed to be the carrot)
    largest_contour = max(contours, key=cv2.contourArea)

    # Segment the coin using Hough Circle Transform
    gray_for_coin = cv2.medianBlur(gray, 5)
    circles = cv2.HoughCircles(
        gray_for_coin, cv2.HOUGH_GRADIENT, dp=1.2, minDist=100,
        param1=50, param2=30, minRadius=10, maxRadius=100
    )

    # Create a mask for the coin
    mask_coin = np.zeros_like(gray)
    coin_detected = False
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        x_coin, y_coin, r_coin = circles[0]
        cv2.circle(mask_coin, (x_coin, y_coin), r_coin, 255, -1)
        coin_detected = True
    else:
        print("Warning: Coin not detected!")

    # Combine masks for display (but keep them separate for annotation)
    display_mask = cv2.bitwise_or(combined_mask, mask_coin)

    # Draw the carrot contour and bounding box
    img_contours = img.copy()
    cv2.drawContours(img_contours, [largest_contour], -1, (0, 255, 0), 3)  # Green contour for carrot
    x, y, w, h = cv2.boundingRect(largest_contour)
    cv2.rectangle(img_contours, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Red bounding box for carrot

    # Annotate the coin if detected
    if coin_detected:
        cv2.circle(img_contours, (x_coin, y_coin), r_coin, (255, 0, 0), 3)  # Blue circle for coin
        cv2.putText(img_contours, "Coin", (x_coin - 30, y_coin - r_coin - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    # Add a label for the carrot
    cv2.putText(img_contours, "Carrot", (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # Display the results
    cv2.imshow("Thresholded Image", display_mask)
    cv2.imshow("Carrot and Coin Contour", img_contours)
    print(f"Carrot bounding box x,y,w,h: {x}, {y}, {w}, {h}")
    if coin_detected:
        print(f"Coin center and radius (x,y,r): {x_coin}, {y_coin}, {r_coin}")

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return w, h, img, largest_contour

# Example usage (replace with your image path)
# w, h, img, contour = measure_carrot_length_pixels("vertical_carrot.jpg")
# Example usage (replace with your image path)
# w, h, img, contour = measure_carrot_length_pixels("vertical_carrot.jpg")

# Example usage (replace with your image path)
# w, h, img, contour = measure_carrot_length_pixels("vertical_carrot.jpg")

# Test için (örnek)
# w, h, img, contour = measure_carrot_length_pixels("vertical_carrot.jpg")


def main():
    # Dikey açıdan çekilmiş foto: havucun uzunluğu ölçülecek
    vertical_image_path = "size_calculator/WhatsApp Image 2025-05-19 at 14.08.11-2.jpeg"
    # Yatay açıdan çekilmiş foto: havucun kalınlığı/genişliği ölçülecek
    horizontal_image_path = "size_calculator/WhatsApp Image 2025-05-19 at 14.08.11.jpeg"
    
    # 1 TL çapı piksel olarak bul
    diameter_pixels_vert, img_vert, circle_vert = find_circle_diameter_pixels(vertical_image_path)
    diameter_pixels_horiz, img_horiz, circle_horiz = find_circle_diameter_pixels(horizontal_image_path)
    
    # Ölçek faktörünü hesapla
    scale_vert = TL_DIAMETER_MM / diameter_pixels_vert
    scale_horiz = TL_DIAMETER_MM / diameter_pixels_horiz
    
    # Havucun piksel cinsinden ölçümünü al
    w_vert, h_vert, _, _ = measure_carrot_length_pixels(vertical_image_path)
    w_horiz, h_horiz, _, _ = measure_carrot_length_pixels(horizontal_image_path)
    
    # Dikey fotoğrafta havucun uzunluğu yüksekliği h_vert piksel
    length_mm = h_vert * scale_vert
    # Yatay fotoğrafta havucun çapını genişlik olarak alabiliriz
    diameter_mm = min(w_horiz, h_horiz) * scale_horiz
    
    hypotenuse_pixels = np.sqrt(w_vert**2 + h_vert**2)  # Hipotenüs: sqrt(w^2 + h^2)
    length_mm = hypotenuse_pixels * scale_vert

    # Hacmi silindir olarak hesapla: V = π * (r^2) * h
    radius_mm = diameter_mm / 2
    volume_mm3 = np.pi * (radius_mm**2) * length_mm  # mm^3
    volume_cm3 = volume_mm3 / 1000  # cm^3
    
    # Kütle (gram)
    mass_g = volume_cm3 * CARROT_DENSITY_G_CM3
    
    print(f"Havucun tahmini uzunluğu: {length_mm:.2f} mm")
    print(f"Havucun tahmini çapı: {diameter_mm:.2f} mm")
    print(f"Hacim (silindir varsayımıyla): {volume_cm3:.2f} cm^3")
    print(f"Tahmini kütle: {mass_g:.2f} gram")
    
if __name__ == "__main__":
    main()
