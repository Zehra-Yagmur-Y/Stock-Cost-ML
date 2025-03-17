import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const AddStock = () => {
  const [materialName, setMaterialName] = useState("");
  const [materialCode, setMaterialCode] = useState("");
  const [totalQuantity, setTotalQuantity] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleAddStock = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await axios.post("http://127.0.0.1:8000/stocks/", {
        material_name: materialName,
        material_code: materialCode,
        total_quantity: parseInt(totalQuantity),
      });

      console.log("✅ Stok başarıyla eklendi:", response.data);
      navigate("/stocks"); // Stoklar listesine yönlendir
    } catch (err) {
      console.error("❌ Stok ekleme hatası:", err.response?.data || err.message);
      setError("Stok eklenemedi! Lütfen bilgilerinizi kontrol edin.");
    }
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gray-100">
      <div className="bg-white p-8 rounded-xl shadow-lg w-96">
        <h2 className="text-2xl font-semibold text-center mb-6">📦 Yeni Stok Ekle</h2>

        {error && <p className="text-red-500 text-sm text-center">{error}</p>}

        <form onSubmit={handleAddStock} className="space-y-4">
          <input
            type="text"
            placeholder="Malzeme Adı"
            value={materialName}
            onChange={(e) => setMaterialName(e.target.value)}
            className="w-full px-4 py-2 border rounded-md"
            required
          />
          <input
            type="text"
            placeholder="Malzeme Kodu"
            value={materialCode}
            onChange={(e) => setMaterialCode(e.target.value)}
            className="w-full px-4 py-2 border rounded-md"
            required
          />
          <input
            type="number"
            placeholder="Miktar"
            value={totalQuantity}
            onChange={(e) => setTotalQuantity(e.target.value)}
            className="w-full px-4 py-2 border rounded-md"
            required
          />

          <button
            type="submit"
            className="w-full bg-green-600 text-white py-2 rounded-md hover:bg-green-700 transition"
          >
            ➕ Stok Ekle
          </button>
        </form>
      </div>
    </div>
  );
};

export default AddStock;
