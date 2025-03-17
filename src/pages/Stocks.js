import React, { useEffect, useState } from "react";
import axios from "axios";

const Stocks = () => {
  const [stocks, setStocks] = useState([]);
  const [updateStockId, setUpdateStockId] = useState(null);
  const [newQuantity, setNewQuantity] = useState("");
  const [prevQuantity, setPrevQuantity] = useState(""); // 🔹 Önceki stok miktarını sakla
  const department = localStorage.getItem("department");

  useEffect(() => {
    fetchStocks();
  }, []);

  const fetchStocks = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/stocks/");
      setStocks(response.data);
    } catch (error) {
      console.error("Stokları çekerken hata oluştu:", error);
    }
  };

  // ✅ **Güncelleme Butonuna Basınca Çalışan Fonksiyon**
  const handleUpdateMode = (stock) => {
    setUpdateStockId(stock.id);
    setNewQuantity(stock.total_quantity); // 🔹 Mevcut değeri giriş alanına koy
    setPrevQuantity(stock.total_quantity); // 🔹 Önceki değeri sakla
  };

  // ✅ **Güncelleme İşlemini API'ye Gönderen Fonksiyon**
  const handleUpdateStock = async (stockId) => {
    try {
      await axios.put(`http://127.0.0.1:8000/stocks/${stockId}`, {
        total_quantity: parseInt(newQuantity),
      });

      fetchStocks(); // Listeyi güncelle
      setUpdateStockId(null); // Güncelleme modunu kapat
    } catch (error) {
      console.error("Stok güncellenirken hata oluştu:", error);
    }
  };

  // ✅ **Güncellemeyi İptal Et (Geri Dön)**
  const handleCancelUpdate = () => {
    setNewQuantity(prevQuantity); // 🔹 Eski değeri geri yükle
    setUpdateStockId(null); // 🔹 Güncelleme modundan çık
  };

  // ✅ **Stok Silme Butonu (Onay Uyarısı ile)**
  const handleDeleteStock = async (stockId, stockName) => {
    const confirmDelete = window.confirm(
      `⚠️ "${stockName}" stokunu silmek istediğinize emin misiniz?`
    );

    if (!confirmDelete) return; // ❌ Kullanıcı "Hayır" dediyse silme işlemini durdur

    try {
      await axios.delete(`http://127.0.0.1:8000/stocks/${stockId}`);
      fetchStocks(); // Silindikten sonra listeyi güncelle
    } catch (error) {
      console.error("Stok silinirken hata oluştu:", error);
    }
  };

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">📦 Stok Listesi ({department})</h1>

      <table className="w-full border-collapse border border-gray-300">
        <thead>
          <tr className="bg-gray-200">
            <th className="border border-gray-300 px-4 py-2">Malzeme Adı</th>
            <th className="border border-gray-300 px-4 py-2">Kod</th>
            <th className="border border-gray-300 px-4 py-2">Miktar</th>
            <th className="border border-gray-300 px-4 py-2">Güncelle</th>
            <th className="border border-gray-300 px-4 py-2">Sil</th>
          </tr>
        </thead>
        <tbody>
          {stocks.map((stock) => (
            <tr key={stock.id} className="text-center">
              <td className="border border-gray-300 px-4 py-2">{stock.material_name}</td>
              <td className="border border-gray-300 px-4 py-2">{stock.material_code}</td>
              <td className="border border-gray-300 px-4 py-2">
                {updateStockId === stock.id ? (
                  <input
                    type="number"
                    value={newQuantity}
                    onChange={(e) => setNewQuantity(e.target.value)}
                    className="w-20 px-2 py-1 border rounded-md"
                  />
                ) : (
                  stock.total_quantity
                )}
              </td>
              <td className="border border-gray-300 px-4 py-2">
                {updateStockId === stock.id ? (
                  <>
                    <button
                      onClick={() => handleUpdateStock(stock.id)}
                      className="bg-green-500 text-white px-3 py-1 rounded-md mr-2"
                    >
                      Kaydet
                    </button>
                    <button
                      onClick={handleCancelUpdate}
                      className="bg-gray-500 text-white px-3 py-1 rounded-md"
                    >
                      İptal
                    </button>
                  </>
                ) : (
                  <button
                    onClick={() => handleUpdateMode(stock)}
                    className="bg-blue-500 text-white px-4 py-1 rounded-md"
                  >
                    Güncelle
                  </button>
                )}
              </td>
              <td className="border border-gray-300 px-4 py-2">
                <button
                  onClick={() => handleDeleteStock(stock.id, stock.material_name)}
                  className="bg-red-500 text-white px-4 py-1 rounded-md"
                >
                  Sil
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Stocks;
