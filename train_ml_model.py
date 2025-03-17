import json
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# ✅ JSON'daki verileri yükleyelim
with open("material_variants.json", "r", encoding="utf-8") as f:
    material_variants = json.load(f)

# ✅ Eğitim için veri setini hazırlayalım
X_train = []
y_train = []

for correct_name, wrong_variants in material_variants.items():
    for wrong_name in wrong_variants:
        X_train.append(wrong_name)  # Yanlış isimleri input olarak kullanıyoruz
        y_train.append(correct_name)  # Doğru karşılıklarını hedef olarak belirtiyoruz

# ✅ TF-IDF vektörleştiriciyi oluştur
vectorizer = TfidfVectorizer(ngram_range=(1, 2))  # Unigram ve Bigram kullanıyoruz
X_train_tfidf = vectorizer.fit_transform(X_train)

# ✅ Lojistik Regresyon modeli ile eğit
model = LogisticRegression(max_iter=500)
model.fit(X_train_tfidf, y_train)

# ✅ Modeli ve vektörleştiriciyi kaydet
joblib.dump(vectorizer, "isg_api/tfidf_vectorizer.pkl")
joblib.dump(model, "isg_api/tfidf_correction_model.pkl")

print("✅ TF-IDF Makine Öğrenmesi Modeli başarıyla eğitildi ve kaydedildi.")



#uvicorn isg_api.main:app --reload
