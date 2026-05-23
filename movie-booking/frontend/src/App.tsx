import { useEffect, useState } from "react";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

type Movie = {
  id: number;
  title: string;
  description: string;
  poster_url: string | null;
  duration_minutes: number;
  genre: string;
  rating: string;
};

type User = {
  id: number;
  email: string;
  full_name: string;
  role: string;
};

function App() {
  const [token, setToken] = useState<string | null>(localStorage.getItem("token"));
  const [user, setUser] = useState<User | null>(null);
  const [movies, setMovies] = useState<Movie[]>([]);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [isRegister, setIsRegister] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // โหลดหนัง
  useEffect(() => {
    fetch(`${API}/movies`)
      .then((r) => r.json())
      .then(setMovies)
      .catch(() => setError("ไม่สามารถโหลดหนังได้"));
  }, []);

  // ดึง user ถ้ามี token
  useEffect(() => {
    if (!token) {
      setUser(null);
      return;
    }
    fetch(`${API}/auth/me`, { headers: { Authorization: `Bearer ${token}` } })
      .then((r) => (r.ok ? r.json() : null))
      .then((u) => {
        if (u) setUser(u);
        else handleLogout();
      });
  }, [token]);

  const handleLogin = async () => {
    setError("");
    setLoading(true);
    try {
      const form = new FormData();
      form.append("username", email);
      form.append("password", password);
      const res = await fetch(`${API}/auth/login`, { method: "POST", body: form });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Login failed");
      setToken(data.access_token);
      localStorage.setItem("token", data.access_token);
      setEmail("");
      setPassword("");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Login failed");
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async () => {
    setError("");
    setLoading(true);
    try {
      const res = await fetch(`${API}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password, full_name: fullName }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Register failed");
      // auto login
      await handleLogin();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Register failed");
      setLoading(false);
    }
  };

  const handleLogout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem("token");
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 p-4 sticky top-0 z-10">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <h1 className="text-2xl font-bold">🎬 Movie Booking</h1>
          {user ? (
            <div className="flex items-center gap-3">
              <span className="text-sm">
                สวัสดี <strong>{user.full_name}</strong>
                {user.role === "admin" && (
                  <span className="ml-2 px-2 py-0.5 bg-yellow-500 text-black text-xs rounded">
                    ADMIN
                  </span>
                )}
              </span>
              <button
                onClick={handleLogout}
                className="px-3 py-1 bg-red-600 hover:bg-red-700 rounded text-sm"
              >
                ออกจากระบบ
              </button>
            </div>
          ) : (
            <span className="text-sm text-gray-400">ยังไม่ได้ login</span>
          )}
        </div>
      </header>

      <main className="max-w-6xl mx-auto p-6">
        {/* Login / Register Form */}
        {!user && (
          <div className="bg-gray-800 rounded-lg p-6 mb-8 max-w-md mx-auto">
            <div className="flex gap-2 mb-4">
              <button
                onClick={() => setIsRegister(false)}
                className={`flex-1 py-2 rounded ${
                  !isRegister ? "bg-blue-600" : "bg-gray-700"
                }`}
              >
                เข้าสู่ระบบ
              </button>
              <button
                onClick={() => setIsRegister(true)}
                className={`flex-1 py-2 rounded ${
                  isRegister ? "bg-blue-600" : "bg-gray-700"
                }`}
              >
                สมัครสมาชิก
              </button>
            </div>

            <div className="space-y-3">
              {isRegister && (
                <input
                  type="text"
                  placeholder="ชื่อ-นามสกุล"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="w-full px-3 py-2 bg-gray-700 rounded border border-gray-600 focus:border-blue-500 focus:outline-none"
                />
              )}
              <input
                type="email"
                placeholder="อีเมล"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3 py-2 bg-gray-700 rounded border border-gray-600 focus:border-blue-500 focus:outline-none"
              />
              <input
                type="password"
                placeholder="รหัสผ่าน"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3 py-2 bg-gray-700 rounded border border-gray-600 focus:border-blue-500 focus:outline-none"
              />

              {error && (
                <div className="bg-red-900 border border-red-700 text-red-200 p-2 rounded text-sm">
                  {error}
                </div>
              )}

              <button
                onClick={isRegister ? handleRegister : handleLogin}
                disabled={loading}
                className="w-full py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 rounded font-semibold"
              >
                {loading ? "กำลังโหลด..." : isRegister ? "สมัคร" : "เข้าสู่ระบบ"}
              </button>

              <p className="text-xs text-gray-400 text-center">
                ทดลอง: user@movie.com / user123 (หรือ admin@movie.com / admin123)
              </p>
            </div>
          </div>
        )}

        {/* Movies Grid */}
        <h2 className="text-2xl font-bold mb-4">🎞️ หนังที่กำลังฉาย</h2>
        {movies.length === 0 ? (
          <p className="text-gray-400">ยังไม่มีหนัง</p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {movies.map((m) => (
              <div
                key={m.id}
                className="bg-gray-800 rounded-lg overflow-hidden hover:ring-2 hover:ring-blue-500 transition"
              >
                {m.poster_url && (
                  <img
                    src={m.poster_url}
                    alt={m.title}
                    className="w-full h-80 object-cover"
                  />
                )}
                <div className="p-4">
                  <h3 className="text-lg font-bold mb-1">{m.title}</h3>
                  <div className="flex gap-2 text-xs text-gray-400 mb-2">
                    <span>{m.genre}</span>
                    <span>•</span>
                    <span>{m.duration_minutes} นาที</span>
                    <span>•</span>
                    <span className="px-1 bg-gray-700 rounded">{m.rating}</span>
                  </div>
                  <p className="text-sm text-gray-300 line-clamp-3">{m.description}</p>
                  {user && (
                    <button
                      className="mt-3 w-full py-2 bg-blue-600 hover:bg-blue-700 rounded text-sm font-semibold"
                      onClick={() => alert(`🚧 ฟีเจอร์จองตั๋วกำลังพัฒนา (${m.title})`)}
                    >
                      จองตั๋ว
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}

        <footer className="mt-12 text-center text-gray-500 text-sm">
          Movie Booking System • DevOps Project
        </footer>
      </main>
    </div>
  );
}

export default App;
