import joblib
from rapidfuzz import process

# ✅ Model ve vektörleştiriciyi yükle
try:
    vectorizer = joblib.load("isg_api/tfidf_vectorizer.pkl")
    ml_model = joblib.load("isg_api/tfidf_correction_model.pkl")
    ml_correction_model = joblib.load("isg_api/material_correction_model.pkl")
except FileNotFoundError as e:
    print(f"❌ Model yükleme hatası: {e}")
    vectorizer = None
    ml_model = None
    ml_correction_model = None

# ✅ RapidFuzz için mevcut malzeme isimlerini yükle
existing_names = [
    "Gloves", "Helmet", "Safety Glasses", "Ear Protection",
    "Safety Shoes", "Face Shield", "Protective Suit",
    "Fire Resistant Jacket", "Respirator Mask"
]

def correct_material_name(input_name):
    """
    1️⃣ RapidFuzz → 2️⃣ TF-IDF ML Modeli → 3️⃣ AI API Kullanımı 
    """

    print(f"🔍 Gelen isim: {input_name}")

    # 1️⃣ RapidFuzz ile eşleşme kontrolü
    best_match, score, _ = process.extractOne(input_name, existing_names)
    print(f"🔍 RapidFuzz Skoru: {input_name} → {best_match} ({score})")

    if score > 80:  # Eğer eşleşme %85'ten büyükse, RapidFuzz önerisini döndür
        print(f"✅ RapidFuzz Düzeltmesi: {input_name} → {best_match}")
        return best_match

    # 2️⃣ TF-IDF + ML Modeli ile eşleşme kontrolü
    if vectorizer and ml_model:
        input_tfidf = vectorizer.transform([input_name])  # İsmi vektörleştir
        predicted_name = ml_model.predict(input_tfidf)[0]  # Model ile tahmin et
        print(f"🤖 ML Model Tahmini: {input_name} → {predicted_name}")

        if predicted_name.lower() != input_name.lower():
            print(f"✅ ML Modeli Düzeltmesi: {input_name} → {predicted_name}")
            return predicted_name

    # 3️⃣ Eğer hala emin değilsek, AI API'yi çağır (Gemini veya DeepSeek)
    if ml_correction_model:
        corrected_name = ml_correction_model.correct_material_name(input_name)
        print(f"✅ AI API Düzeltmesi: {input_name} → {corrected_name}")
        return corrected_name

    # Eğer hiçbir düzeltme yapılamazsa, orijinal değeri döndür
    print(f"⚠️ Düzeltme yapılamadı, orijinal değer döndü: {input_name}")
    return input_name
