from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.routers import auth, cinemas, movies

settings = get_settings()

app = FastAPI(
    title="Movie Booking API",
    version="0.1.0",
    description="ระบบจองตั๋วหนัง",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(movies.router)
app.include_router(cinemas.router)


@app.get("/", tags=["Health"])
def root() -> dict[str, str]:
    return {"message": "Movie Booking API"}


@app.get("/health", tags=["Health"])
def health(db: Session = Depends(get_db)) -> dict[str, str]:
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": str(e)}
