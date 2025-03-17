import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Stocks from "./pages/Stocks";
import AddStock from "./pages/AddStock"; // ✅ Yeni stok ekleme sayfasını ekledik
import Reports from "./pages/Reports";  // ✅ **Yeni Sayfa İçeri Aktarıldı**

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/stocks" element={<Stocks />} />
        <Route path="/add-stock" element={<AddStock />} /> {/* ✅ Yeni stok ekleme rotası */}
        <Route path="/reports" element={<Reports />} />  {/* ✅ **Raporlar Sayfası Eklendi** */}
      </Routes>
    </Router>
  );
}

export default App;
