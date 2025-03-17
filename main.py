from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from isg_api.database import SessionLocal, get_db, Base, engine
from isg_api import models, schemas, crud
from isg_api.utils import correct_material_name  # ✅ ML fonksiyonunu dahil ettik
from isg_api.models import User, MainStock
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 🔥 CORS Middleware ekleyelim:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔥 Tüm kaynaklardan isteklere izin ver
    allow_credentials=True,
    allow_methods=["*"],  # 🔥 Tüm HTTP metodlarına izin ver (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # 🔥 Tüm başlıklara izin ver
)

# ✅ Veritabanı tablolarını oluştur (Eğer yoksa)
Base.metadata.create_all(bind=engine)

# ✅ Kullanıcı giriş modeli
class LoginRequest(BaseModel):
    username: str
    password: str
    department: str  # 🔹 Bölüm bilgisi eklendi

# ✅ Kullanıcı kayıt modeli
class RegisterRequest(BaseModel):
    username: str
    password: str
    department: str  # 🔹 Bölüm bilgisi ekleniyor

# ✅ Kullanıcı kayıt endpointi
@app.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == request.username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Bu kullanıcı adı zaten kullanılıyor!")

    # ✅ Yeni kullanıcıyı ekle
    new_user = User(
        username=request.username,
        password=request.password,  # ❗ Şifreyi hashlemeyi ileride ekleyelim!
        department=request.department
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Kullanıcı başarıyla oluşturuldu!",
        "username": new_user.username,
        "department": new_user.department
    }

# ✅ Kullanıcı giriş endpointi
@app.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """ Kullanıcı girişini doğrular ve token döndürür """
    user = db.query(models.User).filter(models.User.username == request.username).first()

    if not user or user.password != request.password:
        raise HTTPException(status_code=401, detail="Geçersiz kullanıcı adı veya şifre")

    return {
        "token": f"mock-token-{user.id}",
        "username": user.username,
        "department": request.department  # 🔹 Departman bilgisini ekledik
    }

# ✅ Root Endpoint
@app.get("/")
def home():
    return {"message": "ISG Stok API Çalışıyor 🚀"}

# ✅ Stok ekleme (POST)
@app.post("/stocks/", response_model=schemas.MainStockRead)
def create_stock(stock: schemas.MainStockCreate, db: Session = Depends(get_db)):
    return crud.create_stock(db=db, stock=stock)

# ✅ Tüm stokları getirme (GET)
@app.get("/stocks/", response_model=list[schemas.MainStockRead])
def get_all_stocks(db: Session = Depends(get_db)):
    return crud.get_stocks(db=db)

# ✅ Belirli bir stok kaydını getirme (GET /{id})
@app.get("/stocks/{stock_id}", response_model=schemas.MainStockRead)
def get_stock(stock_id: int, db: Session = Depends(get_db)):
    stock = crud.get_stock_by_id(db=db, stock_id=stock_id)
    if stock is None:
        raise HTTPException(status_code=404, detail="Stok bulunamadı")
    return stock

# ✅ Güncelleme için Pydantic Modeli
class UpdateStockRequest(BaseModel):
    total_quantity: int  # Yeni miktarı belirtiyoruz

# ✅ Stok Güncelleme (PUT)
@app.put("/stocks/{stock_id}")
def update_stock(stock_id: int, request: UpdateStockRequest, db: Session = Depends(get_db)):
    stock = db.query(MainStock).filter(MainStock.id == stock_id).first()

    if not stock:
        raise HTTPException(status_code=404, detail="Stok bulunamadı!")

    stock.total_quantity = request.total_quantity  # Yeni miktarı güncelle
    db.commit()
    db.refresh(stock)
    
    return {
        "message": "Stok başarıyla güncellendi!",
        "material_name": stock.material_name,
        "new_quantity": stock.total_quantity
    }

# ✅ Stok Silme Endpointi (Güncellenmiş Hali)
@app.delete("/stocks/{stock_id}")
def delete_stock(stock_id: int, db: Session = Depends(get_db)):
    stock = db.query(models.MainStock).filter(models.MainStock.id == stock_id).first()

    if not stock:
        raise HTTPException(status_code=404, detail="Stok bulunamadı!")

    db.delete(stock)
    db.commit()
    
    return {"message": f"Stok başarıyla silindi: {stock.material_name}"}

# ✅ Yeni Eklenen Endpoint: Malzeme İsmi Düzeltme (ML Modeli Kullanarak)
@app.post("/predict-material/")
def predict_material(material_name: str):
    """ Yanlış girilen malzeme ismini düzeltir """
    corrected_name = correct_material_name(material_name)
    return {"original_name": material_name, "corrected_name": corrected_name}
