import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:8000";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [department, setDepartment] = useState("Body"); // Varsayılan olarak Body seçili
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await axios.post(`${API_BASE_URL}/login`, {
        username,
        password,
        department,
      });

      console.log("✅ API Yanıtı:", response.data); // ✅ API Yanıtını Konsola Yazdır

      if (response.data.token) {
        // ✅ Kullanıcı bilgilerini localStorage'e kaydet
        localStorage.setItem("token", response.data.token);
        localStorage.setItem("username", response.data.username);
        localStorage.setItem("department", response.data.department);

        // ✅ Giriş başarılı, yönlendir
        navigate("/stocks");
      } else {
        setError("Geçersiz giriş bilgileri!");
      }
    } catch (err) {
      console.error("❌ Giriş hatası:", err.response?.data || err.message); // ✅ Hata Mesajı Detaylı Göster
      setError("Giriş başarısız. Lütfen tekrar deneyin.");
    }
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gray-100">
      <div className="bg-white p-8 rounded-xl shadow-lg w-96">
        <h2 className="text-2xl font-semibold text-center mb-6">Giriş Yap</h2>

        {error && <p className="text-red-500 text-sm text-center">{error}</p>}

        <form onSubmit={handleLogin} className="space-y-4">
          <input
            type="text"
            placeholder="Kullanıcı Adı"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full px-4 py-2 border rounded-md"
            required
          />
          <input
            type="password"
            placeholder="Şifre"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-2 border rounded-md"
            required
          />

          {/* 🔹 Bölüm Seçimi Dropdown */}
          <select
            value={department}
            onChange={(e) => setDepartment(e.target.value)}
            className="w-full px-4 py-2 border rounded-md"
          >
            <option value="Body">Body</option>
            <option value="Press">Press</option>
            <option value="Kaynak">Kaynak</option>
            <option value="Cost">Cost (Analiz Ekibi)</option>
          </select>

          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition"
          >
            Giriş Yap
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;
