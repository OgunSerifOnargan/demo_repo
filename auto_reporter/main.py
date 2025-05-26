import requests
import time
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import os

#commit try
#branch try

def extract_audio_with_silence(video_path, output_audio_path, silence_duration_ms=5000):
    # Geçici bir dosya adı belirle
    temp_audio_path = "temp_audio.mp3"

    # 1. Videodan sesi çıkar
    print("[INFO] Videodan ses çıkartılıyor...")
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(temp_audio_path, codec='libmp3lame')

    # 2. Pydub ile sesi yükle
    print("[INFO] Çıkartılan ses yükleniyor...")
    audio = AudioSegment.from_mp3(temp_audio_path)

    # 3. Sessizlik oluştur ve başa ekle
    print(f"[INFO] {silence_duration_ms/1000} saniyelik sessizlik ekleniyor...")
    silence = AudioSegment.silent(duration=silence_duration_ms)
    final_audio = silence + audio

    # 4. Son halini mp3 olarak kaydet
    print(f"[INFO] Final ses dosyası kaydediliyor: {output_audio_path}")
    final_audio.export(output_audio_path, format="mp3")

    # 5. Geçici dosyayı temizle
    if os.path.exists(temp_audio_path):
        os.remove(temp_audio_path)
    print("[INFO] İşlem tamamlandı.")

def upload_audio(audio_path, api_key):
    headers = {
        'authorization': api_key,
        'content-type': 'application/octet-stream'
    }
    with open(audio_path, 'rb') as f:
        response = requests.post(
            'https://api.assemblyai.com/v2/upload',
            headers=headers,
            data=f
        )
    return response.json()['upload_url']

def start_transcription(audio_url, api_key):
    endpoint = "https://api.assemblyai.com/v2/transcript"
    json_data = {
        'audio_url': audio_url,
        'language_code': 'tr'  # Türkçe dil seçimi
    }
    headers = {
        "authorization": api_key,
        "content-type": "application/json"
    }
    response = requests.post(endpoint, json=json_data, headers=headers)
    return response.json()['id']


# 4. Transkripsiyon sonucunu al
def get_transcription_result(transcript_id, api_key):
    endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    headers = {"authorization": api_key}
    
    while True:
        response = requests.get(endpoint, headers=headers)
        result = response.json()
        
        if result['status'] == 'completed':
            return result['text']
        elif result['status'] == 'error':
            raise Exception("Transkripsiyon hatası:", result['error'])
        time.sleep(3)

# 🔧 KULLANIM
if __name__ == "__main__":
    API_KEY = "100a90a92d374258881e7cb9fb187016"
    video_file = "test_video/WhatsApp Video 2025-05-15 at 14.03.47.mp4"
    audio_file = "audios/audio.mp3"

    extract_audio_with_silence(video_file, audio_file, silence_duration_ms=5000)
    audio_url = upload_audio(audio_file, API_KEY)
    transcript_id = start_transcription(audio_url, API_KEY)
    text = get_transcription_result(transcript_id, API_KEY)
    
    print("Transkripte edilen metin:\n")
    print(text)
    # Metni dosyaya yaz
    with open("transcription.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("Transkript başarıyla 'transcription.txt' dosyasına yazıldı.")

