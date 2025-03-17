import json
import joblib
from rapidfuzz import process

class MaterialCorrectionModel:
    def __init__(self):
        #  JSON dosyasını yükleNDİ
        try:
            with open("material_variants.json", "r", encoding="utf-8") as f:
                self.material_variants = json.load(f)
        except FileNotFoundError:
            print("❌ material_variants.json bulunamadı! Model oluşturulamadı.")
            self.material_variants = {}

        self.correct_names = list(self.material_variants.keys())

    def correct_material_name(self, input_name):
        """Yanlış malzeme ismini en yakın doğru malzeme ismiyle düzeltir."""
        if input_name in self.correct_names:
            return input_name
        
        #  RapidFuzz ile en iyi eşleşmeyi bul
        match_result = process.extractOne(input_name, self.correct_names)
        if match_result is None:
            return input_name  # Hiçbir eşleşme bulunamadıysa orijinalini döndür
        
        best_match, score, _ = match_result
        
        return best_match if score > 75 else input_name  # %80 eşleşme eşiği

#  Modeli oluştur ve kaydet
model = MaterialCorrectionModel()
joblib.dump(model, "isg_api/material_correction_model.pkl")

print("✅ Model başarıyla kaydedildi: isg_api/material_correction_model.pkl")

#  Test için örnek yanlış malzeme isimleri
test_names = ["gloues", "hlemet", "reapirator mask", "fire resismtant jacket"]

print("\n Model Test Sonuçları:")
for name in test_names:
    corrected_name = model.correct_material_name(name)
    print(f"❌ Yanlış: {name}  ✅ Düzeltilmiş: {corrected_name}")

#uvicorn isg_api.main:app --host 127.0.0.1 --port 8000 –reload 
#source venv/Scripts/activate