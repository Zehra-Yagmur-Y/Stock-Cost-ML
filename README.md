# Stock-Cost-ML
Machine Learning-Based Stock and Cost Optimization

##  Overview
 Stock Management System is a web application designed for factory stock management. The system allows different departments (**Body, Press, Welding, Cost**) to manage their stocks efficiently. The **Cost Analysis** team evaluates stock changes on a monthly basis and generates reports.

##  Technologies Used
- **Frontend:** React.js, Tailwind CSS, Recharts
- **Backend:** FastAPI, SQLAlchemy
- **Database:** PostgreSQL
- **Authentication:** JWT Token, Bcrypt (Password Hashing)
- **Data Processing:** Natural Language Processing (NLP), RapidFuzz (Material Name Normalization)

##  Features
###  Stock Management
- Add, update, and delete stock items
- View stock levels filtered by department
- Automatic correction of material names

###  Reporting & Analysis (For Cost Team)
- Stock change visualization (Bar & Pie charts)
- Most used materials
- Monthly stock variation
- Low stock alerts

###  Authentication & Authorization
- Secure login with **JWT authentication**
- Password hashing with **Bcrypt**
- Role-based access (Only Cost Team can access reports)

##  Installation & Setup
### **Backend Setup**
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo-url.git
   cd isg-stock-management
   ```
2. Create a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up PostgreSQL database:
   ```sh
   psql -U postgres -c "CREATE DATABASE factory_stock;"
   ```
5. Run the FastAPI server:
   ```sh
   uvicorn isg_api.main:app --reload
   ```

### **Frontend Setup**
1. Navigate to the frontend folder:
   ```sh
   cd isg-stock-frontend
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Start the React application:
   ```sh
   npm start
   ```

##  API Endpoints
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST   | /register | Register a new user |
| POST   | /login | User login (JWT) |
| GET    | /stocks | Retrieve all stocks |
| POST   | /stocks | Add new stock |
| PUT    | /stocks/{id} | Update stock quantity |
| DELETE | /stocks/{id} | Delete a stock item |
| GET    | /reports/stats | Get stock reports (Only for Cost Team) |

##  Authentication
- Users must log in with a username and password.
- Passwords are securely stored using **Bcrypt hashing**.
- Only authorized users can access specific routes.

##  Contributions
Pull requests are welcome! If you find any issues, feel free to report them.

---


##  Genel Bakış
 Stok Yönetim Sistemi, fabrikalar için tasarlanmış bir web tabanlı stok yönetim sistemidir. **Body, Press, Kaynak ve Cost** gibi bölümler, stoklarını verimli bir şekilde yönetebilir. **Cost Analiz** ekibi ise stok değişimlerini aylık olarak değerlendirir ve raporlar oluşturur.

##  Kullanılan Teknolojiler
- **Frontend:** React.js, Tailwind CSS, Recharts
- **Backend:** FastAPI, SQLAlchemy
- **Veritabanı:** PostgreSQL
- **Kimlik Doğrulama:** JWT Token, Bcrypt (Şifre Hashleme)
- **Veri İşleme:** Doğal Dil İşleme (NLP), RapidFuzz (Malzeme İsmi Normalizasyonu)

##  Özellikler
###  Stok Yönetimi
- Stok ekleme, güncelleme ve silme
- Bölüme göre stokları listeleme
- Otomatik malzeme adı düzeltme

###  Raporlama & Analiz (Cost Ekibi İçin)
- Stok değişimlerini görselleştirme (Bar & Pie grafikleri)
- En çok tüketilen malzemeler
- Aylık stok değişimleri
- Kritik stok uyarıları

###  Kimlik Doğrulama & Yetkilendirme
- **JWT kimlik doğrulama** ile güvenli giriş
- **Bcrypt ile şifre hashleme**
- Rol bazlı erişim (Sadece Cost Ekibi raporları görebilir)

##  Kurulum & Kullanım
### **Backend Kurulumu**
1. Repoyu klonlayın:
   ```sh
   git clone https://github.com/your-repo-url.git
   cd isg-stock-management
   ```
2. Sanal ortam oluşturun:
   ```sh
   python -m venv venv
   source venv/bin/activate  # Windows için: venv\Scripts\activate
   ```
3. Bağımlılıkları yükleyin:
   ```sh
   pip install -r requirements.txt
   ```
4. PostgreSQL veritabanını oluşturun:
   ```sh
   psql -U postgres -c "CREATE DATABASE factory_stock;"
   ```
5. FastAPI sunucusunu çalıştırın:
   ```sh
   uvicorn isg_api.main:app --reload
   ```

### **Frontend Kurulumu**
1. Frontend klasörüne gidin:
   ```sh
   cd isg-stock-frontend
   ```
2. Bağımlılıkları yükleyin:
   ```sh
   npm install
   ```
3. React uygulamasını başlatın:
   ```sh
   npm start
   ```

##  API Endpointleri
| Yöntem | Endpoint | Açıklama |
|--------|---------|----------|
| POST   | /register | Yeni kullanıcı kaydı |
| POST   | /login | Kullanıcı girişi (JWT) |
| GET    | /stocks | Tüm stokları getir |
| POST   | /stocks | Yeni stok ekle |
| PUT    | /stocks/{id} | Stok miktarını güncelle |
| DELETE | /stocks/{id} | Stok sil |
| GET    | /reports/stats | Stok raporlarını getir (Sadece Cost Ekibi) |

##  Kimlik Doğrulama
- Kullanıcılar giriş yapmak için **kullanıcı adı ve şifre** girmelidir.
- Şifreler **Bcrypt hashleme** ile güvenli şekilde saklanır.
- Yetkili kullanıcılar yalnızca belirli sayfalara erişebilir.

##  Katkıda Bulunma
Pull request'ler kabul edilir! Eğer bir hata bulursanız, bildirin. 😊

