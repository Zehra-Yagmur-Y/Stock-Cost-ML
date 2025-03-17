import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#  .env dosyasını yükle
load_dotenv()

# DATABASE_URL çevresel değişkenini oku
DATABASE_URL = os.getenv("DATABASE_URL")

#  Eğer .env dosyası eksikse, varsayılan bir bağlantı adresi kullan
if DATABASE_URL is None:
    print("⚠️ Uyarı: DATABASE_URL bulunamadı! Varsayılan bağlantı kullanılıyor.")
    DATABASE_URL = "postgresql://postgres:123456@localhost:5432/factory_stock"

#  Veritabanı bağlantısını oluştur
engine = create_engine(DATABASE_URL, echo=True)  # echo=True -> SQL sorgularını gösterir

#  Oturum yönetimi (Session)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#  SQLAlchemy ORM için Base sınıfı
Base = declarative_base()

#  Veritabanı oturumu çağırmak için fonksiyon
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
