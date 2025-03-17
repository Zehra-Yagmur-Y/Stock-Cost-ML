from sqlalchemy.orm import Session
from isg_api.models import MainStock
from isg_api.schemas import MainStockCreate
from isg_api.utils import correct_material_name  # ML Modelini içe aktar
from rapidfuzz import process  

#  Mevcut malzeme isimlerini kontrol eden normalizasyon fonksiyonu
def normalize_material_name(db: Session, input_name: str) -> str:
    existing_names = [stock.material_name for stock in db.query(MainStock).all()]
    print(f" Mevcut malzeme isimleri: {existing_names}")  # Debug için

    if not existing_names:
        return input_name  # Eğer veritabanı boşsa, doğrudan ekle

    # 🔹 Önce makine öğrenmesi modelinden düzeltme önerisi al
    corrected_name = correct_material_name(input_name)
    print(f" Model Düzeltmesi: {input_name} → {corrected_name}")

    #  Eğer modelin önerisi zaten veri tabanında varsa direkt onu kullan
    if corrected_name in existing_names:
        return corrected_name  

    # 🔹 RapidFuzz ile en yakın eşleşmeyi bul
    match_result = process.extractOne(input_name, existing_names)

    if match_result is None:
        return corrected_name  # Model önerisini kullan

    best_match, score, _ = match_result  
    print(f" En iyi eşleşme: {best_match} (Skor: {score})")  

    # **Karar Mekanizması:** 
    # - Eğer RapidFuzz'un skoru çok yüksekse (85+), onu kullan.
    # - Eğer modelin önerisi güçlü ve RapidFuzz farklı bir şey öneriyorsa, modelin önerisini kullan.
    if score > 85:
        return best_match
    else:
        return corrected_name


#  Stok ekleme (POST) - Aynı malzeme varsa miktarını artır
def create_stock(db: Session, stock: MainStockCreate):
    try:
        normalized_name = normalize_material_name(db, stock.material_name)

        #  Aynı isimde malzeme varsa, toplam miktarı artır
        existing_stock = db.query(MainStock).filter(MainStock.material_name == normalized_name).first()

        if existing_stock:
            existing_stock.total_quantity += stock.total_quantity
            db.commit()
            db.refresh(existing_stock)
            print(f"🔄 {normalized_name} miktarı artırıldı: {existing_stock.total_quantity}")
            return existing_stock  # Güncellenmiş kayıt döndür

        #  Eğer yoksa, yeni kayıt ekle
        db_stock = MainStock(
            material_name=normalized_name,
            material_code=stock.material_code,
            total_quantity=stock.total_quantity
        )
        db.add(db_stock)
        db.commit()
        db.refresh(db_stock)
        print(f" Yeni malzeme eklendi: {normalized_name}")
        return db_stock

    except Exception as e:
        db.rollback()  # Hata durumunda işlemi geri al
        print(f"❌ Stok eklenirken hata oluştu: {str(e)}")
        raise ValueError(f"Stok eklenirken hata oluştu: {str(e)}")


#  Tüm stokları getir (GET)
def get_stocks(db: Session):
    return db.query(MainStock).all()


#  Belirli bir stok kaydını ID'ye göre getir (GET)
def get_stock_by_id(db: Session, stock_id: int):
    return db.query(MainStock).filter(MainStock.id == stock_id).first()


#  Stok güncelleme (PUT)
def update_stock(db: Session, stock_id: int, stock_update: MainStockCreate):
    stock = db.query(MainStock).filter(MainStock.id == stock_id).first()
    if not stock:
        return None  # Stok bulunamadı

    try:
        stock.material_name = normalize_material_name(db, stock_update.material_name)
        stock.material_code = stock_update.material_code
        stock.total_quantity = stock_update.total_quantity

        db.commit()
        db.refresh(stock)
        print(f" Stok güncellendi: {stock.material_name}")
        return stock

    except Exception as e:
        db.rollback()  # Hata durumunda işlemi geri al
        print(f"❌ Stok güncellenirken hata oluştu: {str(e)}")
        raise ValueError(f"Stok güncellenirken hata oluştu: {str(e)}")


#  Stok silme (DELETE)
def delete_stock(db: Session, stock_id: int):
    stock = db.query(MainStock).filter(MainStock.id == stock_id).first()
    if not stock:
        return None  # Stok bulunamadı

    try:
        db.delete(stock)
        db.commit()
        print(f" Stok silindi: {stock.material_name}")
        return stock

    except Exception as e:
        db.rollback()
        print(f"❌ Stok silinirken hata oluştu: {str(e)}")
        raise ValueError(f"Stok silinirken hata oluştu: {str(e)}")
