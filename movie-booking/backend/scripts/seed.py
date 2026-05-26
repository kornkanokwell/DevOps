"""Seed sample data — รัน: python -m scripts.seed"""

from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

from passlib.context import CryptContext

from app.database import SessionLocal
from app.models import Cinema, Movie, Showtime, User, UserRole

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def seed() -> None:
    db = SessionLocal()
    try:
        print("🌱 Checking and seeding database...")
        
        # ✦ 1. Check & Seed Users
        admin = db.query(User).filter(User.email == "admin@movie.com").first()
        if not admin:
            admin = User(
                email="admin@movie.com",
                hashed_password=pwd_context.hash("admin123"),
                full_name="Admin User",
                role=UserRole.ADMIN,
            )
            db.add(admin)
            
        user = db.query(User).filter(User.email == "user@movie.com").first()
        if not user:
            user = User(
                email="user@movie.com",
                hashed_password=pwd_context.hash("user123"),
                full_name="Test User",
                role=UserRole.USER,
            )
            db.add(user)

        cinema1 = db.query(Cinema).filter(Cinema.name == "Theater 1").first()
        if not cinema1:
            cinema1 = Cinema(name="Theater 1", rows=8, cols=10)
            db.add(cinema1)
            
        cinema2 = db.query(Cinema).filter(Cinema.name == "IMAX 1").first()
        if not cinema2:
            cinema2 = Cinema(name="IMAX 1", rows=10, cols=12)
            db.add(cinema2)

        movie1 = db.query(Movie).filter(Movie.title == "Inception").first()
        if not movie1:
            movie1 = Movie(
                title="Inception",
                description="ขโมยความฝันจากจิตใต้สำนึก",
                poster_url="https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
                duration_minutes=148,
                genre="Sci-Fi",
                rating="PG-13",
                release_date=date(2010, 7, 16),
            )
            db.add(movie1)
            
        movie2 = db.query(Movie).filter(Movie.title == "Interstellar").first()
        if not movie2:
            movie2 = Movie(
                title="Interstellar",
                description="ภารกิจค้นหาดาวเคราะห์ดวงใหม่",
                poster_url="https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
                duration_minutes=169,
                genre="Sci-Fi",
                rating="PG-13",
                release_date=date(2014, 11, 7),
            )
            db.add(movie2)
        
        db.flush()

        now = datetime.now(timezone.utc).replace(hour=10, minute=0, second=0, microsecond=0)
        
        showtime_data = [
            {"movie_id": movie1.id, "cinema_id": cinema1.id, "start_time": now + timedelta(hours=2), "price": Decimal("220.00")},
            {"movie_id": movie1.id, "cinema_id": cinema2.id, "start_time": now + timedelta(hours=5), "price": Decimal("280.00")},
            {"movie_id": movie2.id, "cinema_id": cinema1.id, "start_time": now + timedelta(days=1, hours=3), "price": Decimal("220.00")},
        ]

        inserted_showtimes_count = 0
        for st in showtime_data:
            exists = db.query(Showtime).filter(
                Showtime.movie_id == st["movie_id"],
                Showtime.cinema_id == st["cinema_id"],
                Showtime.start_time == st["start_time"]
            ).first()
            
            if not exists:
                new_st = Showtime(
                    movie_id=st["movie_id"],
                    cinema_id=st["cinema_id"],
                    start_time=st["start_time"],
                    price=st["price"]
                )
                db.add(new_st)
                inserted_showtimes_count += 1

        db.commit()
        print("Seed process completed successfully")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error during seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()