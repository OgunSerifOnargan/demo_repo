import openai
import base64

# 🔐 OpenAI API anahtarını buraya gir
food_type = "Kayısı"

# 📷 Görseli base64 formatına çevir
def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# 🎯 Görsel dosya yolunu belirt
image_path = "/Users/onarganogun/Downloads/WhatsApp Image 2025-05-22 at 12.24.56.jpeg"
base64_image = encode_image(image_path)

# 🧠 OpenAI GPT-4V'ye görsel ile birlikte soru sor
response = openai.ChatCompletion.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": "You are an expert in quality control of a professional kitchen warehouse."},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": f"Bu görseldeki {food_type} hakkında tazelik raporu hazırlar mısın? Ayrıca içinde bulunduğu kasanın doluluk oranını görselden tahmin eder misin?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ],
    temperature=0.2
)

# 📤 Yanıtı yazdır
print(response["choices"][0]["message"]["content"])
