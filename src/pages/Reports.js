import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { PieChart, Pie, Tooltip, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid } from "recharts";

const Reports = () => {
  const [stocks, setStocks] = useState([]);
  const navigate = useNavigate();
  const department = localStorage.getItem("department"); // Kullanıcının departmanı

  useEffect(() => {
    // ✅ Eğer kullanıcı **Cost değilse**, stok sayfasına yönlendir.
    if (department !== "Cost") {
      alert("🚨 Erişim Engellendi! Sadece Cost bölümü raporları görebilir.");
      navigate("/stocks");
      return;
    }

    fetchStocks();
  }, [department, navigate]);

  const fetchStocks = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/stocks/");
      setStocks(response.data);
    } catch (error) {
      console.error("Stokları çekerken hata oluştu:", error);
    }
  };

  // 🔹 **Bölümlere Göre Stok Dağılımı (Pie Chart)**
  const departmentData = stocks.reduce((acc, stock) => {
    const dept = stock.department || "Diğer"; // Eğer departman bilgisi yoksa "Diğer" yaz
    acc[dept] = (acc[dept] || 0) + stock.total_quantity;
    return acc;
  }, {});

  const pieChartData = Object.keys(departmentData).map((key) => ({
    name: key,
    value: departmentData[key],
  }));

  // 🔹 **En Çok Tüketilen Malzemeler (Bar Chart)**
  const barChartData = stocks
    .sort((a, b) => b.total_quantity - a.total_quantity)
    .slice(0, 5) // En çok 5 malzemeyi göster
    .map((stock) => ({
      name: stock.material_name,
      quantity: stock.total_quantity,
    }));

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">📊 Stok Raporları</h1>

      {/* 🔹 **Bölümlere Göre Stok Dağılımı (Pie Chart)** */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold mb-2">📍 Bölümlere Göre Stok Dağılımı</h2>
        <PieChart width={400} height={300}>
          <Pie data={pieChartData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} fill="#82ca9d">
            {pieChartData.map((_, index) => (
              <Cell key={`cell-${index}`} fill={["#8884d8", "#82ca9d", "#ffc658", "#ff6b6b"][index % 4]} />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </div>

      {/* 🔹 **En Çok Tüketilen Malzemeler (Bar Chart)** */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold mb-2">🔥 En Çok Tüketilen Malzemeler</h2>
        <BarChart width={500} height={300} data={barChartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="quantity" fill="#8884d8" />
        </BarChart>
      </div>
    </div>
  );
};

export default Reports;
