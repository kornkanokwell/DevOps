from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Movie Booking API",
    version="0.1.0",
    description="ระบบจองตั๋วหนัง",
)

# CORS - frontend จะอยู่คนละ origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Movie Booking API"}


@app.get("/health")
def health() -> dict[str, str]:
    # ใช้สำหรับ smoke test ใน CI/CD และ Render health check
    return {"status": "ok"}