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

type Showtime = {
  id: number;
  movie_id: number;
  start_time: string;
  price: number;
  cinema?: { name: string };
};

type BookingResult = {
  booking_code: string;
  total_price: number;
  seats: { seat_row: string; seat_col: number }[];
};

type HistoryBooking = {
  id: number;
  booking_code: string;
  showtime_id: number;
  total_price: number;
  status: string;
  seats: { seat_row: string; seat_col: number }[];
};

const ROWS = ["A", "B", "C", "D", "E"];
const COLS = [1, 2, 3, 4, 5, 6, 7, 8];

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

  const [bookingMovie, setBookingMovie] = useState<Movie | null>(null);
  const [showtimes, setShowtimes] = useState<Showtime[]>([]);
  const [selectedShowtime, setSelectedShowtime] = useState<Showtime | null>(null);
  const [selectedSeats, setSelectedSeats] = useState<{ row: string; col: number }[]>([]);
  const [bookingLoading, setBookingLoading] = useState(false);
  const [bookingError, setBookingError] = useState("");
  const [bookingSuccess, setBookingSuccess] = useState<BookingResult | null>(null);

  const [historyOpen, setHistoryOpen] = useState(false);
  const [bookingsHistory, setBookingsHistory] = useState<HistoryBooking[]>([]);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [historyError, setHistoryError] = useState("");

  const [allShowtimes, setAllShowtimes] = useState<Showtime[]>([]);

  useEffect(() => {
    fetch(`${API}/movies`)
      .then((r) => r.json())
      .then((data) => {
        setMovies(data);
        data.forEach((movie: Movie) => {
          fetch(`${API}/movies/${movie.id}/showtimes`)
            .then((r) => r.json())
            .then((stList) => {
              setAllShowtimes((prev) => {
                const filtered = stList.filter((st: Showtime) => !prev.some((p) => p.id === st.id));
                return [...prev, ...filtered];
              });
            })
            .catch(() => {});
        });
      })
      .catch(() => setError("ไม่สามารถโหลดหนังได้"));
  }, []);

  useEffect(() => {
    if (!token) { setUser(null); return; }
    fetch(`${API}/auth/me`, { headers: { Authorization: `Bearer ${token}` } })
      .then((r) => (r.ok ? r.json() : null))
      .then((u) => { if (u) setUser(u); else handleLogout(); });
  }, [token]);

  const handleLogin = async () => {
    setError(""); setLoading(true);
    try {
      const form = new FormData();
      form.append("username", email);
      form.append("password", password);
      const res = await fetch(`${API}/auth/login`, { method: "POST", body: form });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Login failed");
      setToken(data.access_token);
      localStorage.setItem("token", data.access_token);
      setEmail(""); setPassword("");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Login failed");
    } finally { setLoading(false); }
  };

  const handleRegister = async () => {
    setError(""); setLoading(true);
    try {
      const res = await fetch(`${API}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password, full_name: fullName }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Register failed");
      await handleLogin();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Register failed");
      setLoading(false);
    }
  };

  const handleLogout = () => {
    setToken(null); setUser(null);
    localStorage.removeItem("token");
    setBookingsHistory([]);
  };

  const openBooking = async (movie: Movie) => {
    setBookingMovie(movie);
    setSelectedShowtime(null);
    setSelectedSeats([]);
    setBookingError("");
    setBookingSuccess(null);
    try {
      const res = await fetch(`${API}/movies/${movie.id}/showtimes`);
      if (res.ok) {
        const data = await res.json();
        setShowtimes(data);
        if (data.length > 0) setSelectedShowtime(data[0]);
        
        setAllShowtimes((prev) => {
          const filtered = data.filter((st: Showtime) => !prev.some((p) => p.id === st.id));
          return [...prev, ...filtered];
        });
      } else {
        setShowtimes([]);
      }
    } catch {
      setShowtimes([]);
    }
  };

  const toggleSeat = (row: string, col: number) => {
    setSelectedSeats((prev) => {
      const exists = prev.find((s) => s.row === row && s.col === col);
      if (exists) return prev.filter((s) => !(s.row === row && s.col === col));
      if (prev.length >= 8) return prev;
      return [...prev, { row, col }];
    });
  };

  const handleBooking = async () => {
    if (!selectedShowtime || selectedSeats.length === 0) return;
    setBookingLoading(true); setBookingError("");
    try {
      const res = await fetch(`${API}/bookings`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          showtime_id: selectedShowtime.id,
          seats: selectedSeats.map((s) => ({ seat_row: s.row, seat_col: s.col })),
        }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "จองไม่สำเร็จ");
      setBookingSuccess(data);
    } catch (e) {
      setBookingError(e instanceof Error ? e.message : "จองไม่สำเร็จ");
    } finally { setBookingLoading(false); }
  };

  const closeModal = () => {
    setBookingMovie(null);
    setBookingSuccess(null);
    setSelectedSeats([]);
    setBookingError("");
  };

  const openHistoryModal = async () => {
    setHistoryOpen(true);
    setHistoryLoading(true);
    setHistoryError("");
    try {
      const res = await fetch(`${API}/bookings/me`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (!res.ok) throw new Error("ไม่สามารถดึงข้อมูลประวัติการจองได้");
      const data = await res.json();
      setBookingsHistory(data);
    } catch (e) {
      setHistoryError(e instanceof Error ? e.message : "เกิดข้อผิดพลาด");
    } finally {
      setHistoryLoading(false);
    }
  };

  const getBookingDetails = (showtimeId: number) => {
    const showtime = allShowtimes.find((st) => st.id === showtimeId);
    if (!showtime) return { movieTitle: "ไม่พบข้อมูลหนัง", showtimeText: "ไม่พบข้อมูลรอบฉาย" };
    
    const movie = movies.find((m) => m.id === showtime.movie_id);
    const movieTitle = movie ? movie.title : "ไม่พบข้อมูลหนัง";
    const showtimeText = new Date(showtime.start_time).toLocaleString("th-TH", {
      dateStyle: "short", timeStyle: "short"
    });

    return { movieTitle, showtimeText };
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 p-4 sticky top-0 z-10">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <h1 className="text-2xl font-bold">🎬 Movie Booking</h1>
          {user ? (
            <div className="flex items-center gap-3">
              <span className="text-sm">สวัสดี <strong>{user.full_name}</strong>
                {user.role === "admin" && (
                  <span className="ml-2 px-2 py-0.5 bg-yellow-500 text-black text-xs rounded">ADMIN</span>
                )}
              </span>
              {/* ปุ่มประวัติการจอง */}
              <button 
                onClick={openHistoryModal} 
                className="px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-sm transition">
                📜 ประวัติการจอง
              </button>
              <button onClick={handleLogout} className="px-3 py-1 bg-red-600 hover:bg-red-700 rounded text-sm">
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
              <button onClick={() => setIsRegister(false)} className={`flex-1 py-2 rounded ${!isRegister ? "bg-blue-600" : "bg-gray-700"}`}>เข้าสู่ระบบ</button>
              <button onClick={() => setIsRegister(true)} className={`flex-1 py-2 rounded ${isRegister ? "bg-blue-600" : "bg-gray-700"}`}>สมัครสมาชิก</button>
            </div>
            <div className="space-y-3">
              {isRegister && (
                <input type="text" placeholder="ชื่อ-นามสกุล" value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="w-full px-3 py-2 bg-gray-700 rounded border border-gray-600 focus:border-blue-500 focus:outline-none" />
              )}
              <input type="email" placeholder="อีเมล" value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3 py-2 bg-gray-700 rounded border border-gray-600 focus:border-blue-500 focus:outline-none" />
              <input type="password" placeholder="รหัสผ่าน" value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3 py-2 bg-gray-700 rounded border border-gray-600 focus:border-blue-500 focus:outline-none" />
              {error && <div className="bg-red-900 border border-red-700 text-red-200 p-2 rounded text-sm">{error}</div>}
              <button onClick={isRegister ? handleRegister : handleLogin} disabled={loading}
                className="w-full py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 rounded font-semibold">
                {loading ? "กำลังโหลด..." : isRegister ? "สมัคร" : "เข้าสู่ระบบ"}
              </button>
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
              <div key={m.id} className="bg-gray-800 rounded-lg overflow-hidden hover:ring-2 hover:ring-blue-500 transition">
                {m.poster_url && <img src={m.poster_url} alt={m.title} className="w-full h-80 object-cover" />}
                <div className="p-4">
                  <h3 className="text-lg font-bold mb-1">{m.title}</h3>
                  <div className="flex gap-2 text-xs text-gray-400 mb-2">
                    <span>{m.genre}</span><span>•</span>
                    <span>{m.duration_minutes} นาที</span><span>•</span>
                    <span className="px-1 bg-gray-700 rounded">{m.rating}</span>
                  </div>
                  <p className="text-sm text-gray-300 line-clamp-3">{m.description}</p>
                  {user && (
                    <button onClick={() => openBooking(m)}
                      className="mt-3 w-full py-2 bg-blue-600 hover:bg-blue-700 rounded text-sm font-semibold">
                      จองตั๋ว
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}

        <footer className="mt-12 text-center text-gray-500 text-sm">Movie Booking System • DevOps Project</footer>
      </main>

      {/* Booking Modal */}
      {bookingMovie && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-800 rounded-xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex items-start justify-between mb-4">
                <h2 className="text-xl font-bold">🎟️ จองตั๋ว: {bookingMovie.title}</h2>
                <button onClick={closeModal} className="text-gray-400 hover:text-white text-2xl leading-none ml-4">×</button>
              </div>

              {bookingSuccess ? (
                <div className="text-center py-4">
                  <div className="text-5xl mb-4">✅</div>
                  <h3 className="text-xl font-bold text-green-400 mb-2">จองสำเร็จ!</h3>
                  <div className="bg-gray-700 rounded-lg p-4 mb-4 text-left">
                    <p className="text-sm text-gray-400 mb-1">รหัสการจอง</p>
                    <p className="text-2xl font-mono font-bold text-yellow-400">{bookingSuccess.booking_code}</p>
                    <p className="text-sm text-gray-400 mt-3 mb-1">ที่นั่ง</p>
                    <p className="font-semibold">
                      {bookingSuccess.seats.map((s) => `${s.seat_row}${s.seat_col}`).join(", ")}
                    </p>
                    <p className="text-sm text-gray-400 mt-3 mb-1">ราคารวม</p>
                    <p className="font-semibold text-green-400">฿{Number(bookingSuccess.total_price).toFixed(2)}</p>
                  </div>
                  <button onClick={closeModal} className="w-full py-2 bg-blue-600 hover:bg-blue-700 rounded font-semibold">ปิด</button>
                </div>
              ) : (
                <>
                  {showtimes.length === 0 ? (
                    <div className="text-center py-8">
                      <p className="text-gray-400 text-lg">😔 ยังไม่มีรอบฉายสำหรับหนังเรื่องนี้</p>
                      <button onClick={closeModal} className="mt-4 px-6 py-2 bg-gray-700 hover:bg-gray-600 rounded">ปิด</button>
                    </div>
                  ) : (
                    <>
                      <div className="mb-4">
                        <label className="block text-sm text-gray-400 mb-2">เลือกรอบฉาย</label>
                        <div className="space-y-2">
                          {showtimes.map((st) => (
                            <button key={st.id}
                              onClick={() => { setSelectedShowtime(st); setSelectedSeats([]); }}
                              className={`w-full text-left px-3 py-2 rounded border transition ${
                                selectedShowtime?.id === st.id
                                  ? "border-blue-500 bg-blue-900/30"
                                  : "border-gray-600 bg-gray-700 hover:border-gray-500"
                              }`}>
                              <span className="font-semibold">
                                {new Date(st.start_time).toLocaleString("th-TH", {
                                  dateStyle: "short", timeStyle: "short"
                                })}
                              </span>
                              <span className="text-green-400 ml-3">฿{Number(st.price).toFixed(0)} / ที่นั่ง</span>
                            </button>
                          ))}
                        </div>
                      </div>

                      {selectedShowtime && (
                        <div className="mb-4">
                          <label className="block text-sm text-gray-400 mb-2">
                            เลือกที่นั่ง ({selectedSeats.length} ที่นั่ง)
                          </label>
                          <div className="w-full bg-blue-900/40 border border-blue-700 rounded text-center text-xs text-blue-300 py-1 mb-3">
                            🎬 จอภาพ
                          </div>
                          <div className="space-y-1">
                            {ROWS.map((row) => (
                              <div key={row} className="flex gap-1 items-center">
                                <span className="text-xs text-gray-500 w-4">{row}</span>
                                {COLS.map((col) => {
                                  const isSelected = selectedSeats.some((s) => s.row === row && s.col === col);
                                  return (
                                    <button key={col}
                                      onClick={() => toggleSeat(row, col)}
                                      className={`flex-1 py-2 rounded text-xs font-semibold transition ${
                                        isSelected
                                          ? "bg-blue-600 text-white"
                                          : "bg-gray-700 hover:bg-gray-600 text-gray-300"
                                      }`}>
                                      {col}
                                    </button>
                                  );
                                })}
                              </div>
                            ))}
                          </div>
                          <div className="flex gap-3 mt-2 text-xs text-gray-400">
                            <span className="flex items-center gap-1"><span className="w-3 h-3 bg-gray-700 rounded inline-block"></span>ว่าง</span>
                            <span className="flex items-center gap-1"><span className="w-3 h-3 bg-blue-600 rounded inline-block"></span>เลือกแล้ว</span>
                          </div>
                        </div>
                      )}

                      {selectedSeats.length > 0 && selectedShowtime && (
                        <div className="bg-gray-700 rounded-lg p-3 mb-4 text-sm">
                          <div className="flex justify-between">
                            <span className="text-gray-400">ที่นั่ง:</span>
                            <span>{selectedSeats.map((s) => `${s.row}${s.col}`).join(", ")}</span>
                          </div>
                          <div className="flex justify-between mt-1">
                            <span className="text-gray-400">ราคารวม:</span>
                            <span className="text-green-400 font-bold">
                              ฿{(Number(selectedShowtime.price) * selectedSeats.length).toFixed(2)}
                            </span>
                          </div>
                        </div>
                      )}

                      {bookingError && (
                        <div className="bg-red-900 border border-red-700 text-red-200 p-2 rounded text-sm mb-3">
                          {bookingError}
                        </div>
                      )}

                      <div className="flex gap-2">
                        <button onClick={closeModal} className="flex-1 py-2 bg-gray-700 hover:bg-gray-600 rounded text-sm">ยกเลิก</button>
                        <button
                          onClick={handleBooking}
                          disabled={bookingLoading || selectedSeats.length === 0 || !selectedShowtime}
                          className="flex-1 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed rounded text-sm font-semibold">
                          {bookingLoading ? "กำลังจอง..." : `ยืนยันการจอง (${selectedSeats.length} ที่นั่ง)`}
                        </button>
                      </div>
                    </>
                  )}
                </>
              )}
            </div>
          </div>
        </div>
      )}

      {/* --- ประวัติการจอง Modal --- */}
      {historyOpen && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-800 rounded-xl w-full max-w-2xl max-h-[85vh] flex flex-col">
            <div className="p-6 border-b border-gray-700 flex items-center justify-between">
              <h2 className="text-xl font-bold flex items-center gap-2">📜 ประวัติการจองของคุณ</h2>
              <button onClick={() => setHistoryOpen(false)} className="text-gray-400 hover:text-white text-2xl leading-none">×</button>
            </div>

            <div className="p-6 overflow-y-auto flex-1">
              {historyLoading ? (
                <div className="text-center py-8 text-gray-400">กำลังโหลดประวัติการจอง...</div>
              ) : historyError ? (
                <div className="bg-red-900 border border-red-700 text-red-200 p-3 rounded text-sm">{historyError}</div>
              ) : bookingsHistory.length === 0 ? (
                <div className="text-center py-12 text-gray-400">คุณยังไม่มีประวัติการจองตั๋วภาพยนตร์</div>
              ) : (
                <div className="space-y-4">
                  {bookingsHistory.map((bh) => {
                    const { movieTitle, showtimeText } = getBookingDetails(bh.showtime_id);
                    return (
                      <div key={bh.id} className="bg-gray-700 rounded-lg p-4 border border-gray-600 flex flex-col sm:flex-row justify-between gap-4">
                        <div className="space-y-1">
                          <div className="flex items-center gap-2">
                            <span className="text-xs font-mono px-2 py-0.5 bg-gray-600 text-yellow-400 rounded font-bold">
                              CODE: {bh.booking_code}
                            </span>
                            <span className={`text-xs px-2 py-0.5 rounded uppercase font-semibold ${
                              bh.status === "confirmed" || bh.status === "success" 
                                ? "bg-green-900/60 text-green-300 border border-green-700" 
                                : "bg-yellow-900/60 text-yellow-300 border border-yellow-700"
                            }`}>
                              {bh.status || "Confirmed"}
                            </span>
                          </div>
                          <h4 className="text-lg font-bold text-white pt-1">{movieTitle}</h4>
                          <p className="text-sm text-gray-300">📅 รอบฉาย: {showtimeText}</p>
                          <p className="text-sm text-gray-300">
                            💺 ที่นั่ง: <span className="text-blue-300 font-semibold">{bh.seats.map((s) => `${s.seat_row}${s.seat_col}`).join(", ")}</span>
                          </p>
                        </div>
                        <div className="flex sm:flex-col justify-between sm:justify-center items-end border-t sm:border-t-0 pt-2 sm:pt-0 border-gray-600">
                          <span className="text-xs text-gray-400 sm:mb-1">ราคารวม</span>
                          <span className="text-xl font-bold text-green-400">฿{Number(bh.total_price).toFixed(2)}</span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>

            <div className="p-4 border-t border-gray-700 bg-gray-750 flex justify-end rounded-b-xl">
              <button onClick={() => setHistoryOpen(false)} className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded text-sm font-semibold transition">
                ปิดหน้าต่าง
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;