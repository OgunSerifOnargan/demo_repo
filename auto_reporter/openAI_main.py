import openai

def load_transcript(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def create_prompt(transcript_text):
    prompt = f"""
Adayın adı: Emrah Eren  
Pozisyon: Sommelier

Senaryo Özeti: 
    Aday aşağıda yer alan metinde, önce kendisini tanıtıyor ve ardından üç soruya cevap veriyor. Bu metin, adayın kendini tanıttığı ve sorulara cevap verdiği bir videonun speech to text modelleri ile hazırlanmış bir transcripttir. Senin görevin aşağıda belirtilen unsurları göz önüne alarak çok detaylı bir İK aday değerlendirme raporu oluşturmak. 
    Bu işlemleri yaparken dikkat edilmesi gereken hususlar şunlardır,
        1. Rapor, geçmiş zaman kipiyle değil şimdiki zaman ve geniş zamanla yazılmalıdır. Örneğin “aday kendisini iyi tanıtmıştır” değil, “aday kendisini iyi tanıtır” gibi yazılmalıdır.
        2. Dil profesyonel, ciddi ama açık olmalıdır.
        3. Raporun kısımları mümkün olduğunca madde madde yazılmalıdır.
        4. Raporda determinist olman gerekiyor. Sadece bahsedilen hususlardan, kendinden birşey katmadan, bahsetmen gerekiyor.
        5. Speech-to-text methodu ile transcript hazırlanmasından dolayı adayın telaffuzundan, modelin kapasitesinden veya arka gürültüden dolayı bazı kelimeler yanlış transcripte geçirilmiş olabilir. Bundan dolayı telaffuzu benzer kelimelerin yazıya dökülmüş halinin bozuk olmasını önemseme.

Mülakat soruları:
1. Kırmızı ve beyaz şaraplar için ideal servis sıcaklıkları nelerdir?
2. Teruar nedir ve bir şarabın kalitesine etkisi nasıldır?
3. Dekantasyon ne zaman ve nasıl yapılmalıdır?

Adayın Değerlendirildiği İş İlanı:
    About the job
    Who are we?

    We as Nusr-Et, are a culinary empire that crafted the art of dining with its unique blend of exquisite flavors and theatrical presentation. Renowned for its mastery of fine cuts, Nusr-Et has captivated the taste buds of discerning diners worldwide.

    Nusr-Et boasts an extensive international presence, with around 30 restaurants strategically located in prominent cities across the globe, including New York, London, Dubai, Istanbul, and Miami. The culinary prowess of Nusr-Et is underscored by making each dining experience a celebration of taste and texture.

    Nusr-Et reflects a commitment and dedication to excellence. But this is what meets the eye. Do you want to know what goes on behind the scenes in creating such unforgettable culinary journeys? If your answer is yes, then get ready to get a taste of the fine dining world at Nusr-Et.

    Nusr-Et is actively seeking a talented and dynamic individual to join our team in the capacity of a Sommelier. This exciting opportunity is tailor-made for a high-performing professional who possesses a passion for excellence and a penchant for driving organizational growth. As a key member of our team, the successful candidate will play a pivotal role in shaping the future of our organization.

    Sounds like you? Then read the job description below and apply now.

    What do we look for?
    Min. 3-5 years professional experience in similar positions in high-quality Restaurants,
    Excellent command of written and spoken English,
    A candidate must have a Sommelier Certificate,
    Ability to work in a fast-paced environment,
    High sense of responsibility, adaptability to strict deadlines,
    Great knowledge of all wines

    What will you work on?
    Providing a highly efficient and effective service, educating and recommending customers on Wines with trained skills and expertise, training management and service staff on Wines,
    To have a thorough knowledge of all menu and beverage list offerings,
    To develop Wine list and review sales amounts,
    To control cost center

    What will you work on?
    28.550 TL Net Salary + Service Charge + Tip
    Dining Hall
    Shuttle service for the night closing shift
    Special discounts on your favorite D.ream restaurants and retail brands
    Opportunity to become a part of the ever-popular Nusr-Et aka SaltBae family

    Rapor formatı:  
        1. Adayın genel profili:
            Maddeler halinde yazılacaktır. 
            Örnek Format:
                1. Adayın Genel Profili:
                    - ...
                    - ...
                    ...

        2. Teknik ve profesyonel yetenekleri
            Maddeler halinde yazılacaktır.
            Sadece transcriptin adayın kendini tanıttığı kısmından analiz edilecektir. Bu kısımda adayın sorulara verdiği cevapların içeriğindeki herhangi bir husustan bahsedilmeyecektir.

        3. Deneyimleri ve önceki projeleri  
            Maddeler halinde yazılacaktır.

        4. Güçlü ve Zayıf yönleri 
            Maddeler halinde yazılacaktır.
            Ana 2 alt başlıkta Güçlü Yönleri, Zayıf Yönleri şeklinde yazılacaktır.
            Örnek Format:
                4. Güçlü ve Zayıf Yönleri:
                    Güçlü Yönleri:
                        - ...
                        -...
                        ...

                    Zayıf Yönleri:
                        - ...
                        - ...
                        ...

        5. Sorular ve Sorulara Verdiği Cevaplar:
            Soru değerlendirmelerini gerçekleştirirken adayın vermiş olduğu doğru ve yanlış bilgileri liste halinde vermeni istiyorum. Sommelier mesleğini yapabilmek için bu soru kapsamında adayın bilmesi gereken ama aday tarafından bahsedilmeyen hususları ayrıca belirtmeni istiyorum. Bu kısmın sonunda ise her verilen cevap için bir doğruluk ve bir yeterlilik yüzdesi vermeni istiyorum. 
            
            Örnek Format:
            5. Sorular ve Sorulara Verdiği Cevaplar:
                Soru 1: ...
                    - Doğru Bilgiler: ....
                    - Yanlış Bilgiler: ...
                    - Eksik Bilgiler: ...
                    - Doğruluk Yüzdesi: %...
                    - Yeterlilik Yüzdesi: %...

                Soru 2: ...
                    ...

        6. İşe uygunluk değerlendirmesi
            İş ilanında geçen her gereksinimi teker teker ele al ve hepsinin karılama yüzdesi vererek değerlendir.

            Örnek Format:
                6. İşe Uygunluk Değerlendirmesi:
                    - (Gereksinim1): %... ((Mevcutta olan))
                    ...

        7. GeriBildirim Maili
            Değerlendirme olumsuz sonuçlanmışsa adaya gelişim noktalarını belirten bir mail metni. Eğer aday minimum gereksinimleri karşılıyorsa ve bir sonraki aşamaya geçilecekse, raporda bahsedilmeyen ama sommelier mesleğinde aday hakkında eksik kalan, bahsedilmeyen, ama değerlendirme süreci için kritik olan hususları soracaksın.
            Bu mailin formatını formal yapman gerekiyor.

            Örnek Format:
                7. Geri Bildirim Maili:
                    Sayın ...,

                    ...

                    Saygılarımızla,

                    [İsim]
                    [Pozisyon]

        8. İK Kararı:
            Adaya bu pozisyon için işe alım önerisi yapılıp yapılmadığını belirten kısa bir özet İK kararı hazırla.

- Son olarak, bu pozisyona alınmasını önerip önermediğine dair kısa bir IK raporu hazırlamak.

### İş görüşmesi transkripti:
\"\"\"  
{transcript_text}  
\"\"\"

Sorular listesi ayrıca sağlanacaktır. Şimdi sadece adayın verdiği cevaplara ve genel tavrına göre değerlendirmeni yap.
"""
    return prompt

def get_chatgpt_response(prompt, api_key):
    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",  # ChatGPT-4 kullanıyoruz
        messages=[
            {"role": "system", "content": "Sen çok deneyimli bir insan kaynakları (İK) uzmanısın ve meşhur bir et lokantası için sommelier (şarap uzmanı) pozisyonu için iş görüşmelerini değerlendiriyorsun. Adayların mesleki bilgi düzeyi, iletişim yetkinliği, pozisyona uygunluk derecesi ve profesyonel tavırları üzerine kapsamlı raporlar hazırlamakla görevlisin. Raporların detaylı, profesyonel ve objektif olmalı."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=4000
    )
    return response.choices[0].message["content"]

if __name__ == "__main__":
    # Kendi API anahtarını buraya koy
    API_KEY = "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"

    # Transcript dosyasını oku
    transcript_text = load_transcript("transcription.txt")

    # Promptu oluştur
    prompt = create_prompt(transcript_text)

    # OpenAI'den yanıt al
    evaluation = get_chatgpt_response(prompt, API_KEY)

    # Sonucu ekrana yazdır
    print("📋 İK Değerlendirme Raporu:\n")
    print(evaluation)

    # Sonucu dosyaya da yaz
    with open("evaluation_report.txt", "w", encoding="utf-8") as f:
        f.write(evaluation)
