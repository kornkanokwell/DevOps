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
        # ✦ Users
        admin = User(
            email="admin@movie.com",
            hashed_password=pwd_context.hash("admin123"),
            full_name="Admin User",
            role=UserRole.ADMIN,
        )
        user = User(
            email="user@movie.com",
            hashed_password=pwd_context.hash("user123"),
            full_name="Test User",
            role=UserRole.USER,
        )
        db.add_all([admin, user])

        # ✦ Cinemas
        cinema1 = Cinema(name="Theater 1", rows=8, cols=10)
        cinema2 = Cinema(name="IMAX 1", rows=10, cols=12)
        db.add_all([cinema1, cinema2])

        # ✦ Movies
        movie1 = Movie(
            title="Inception",
            description="ขโมยความฝันจากจิตใต้สำนึก",
            poster_url="https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
            duration_minutes=148,
            genre="Sci-Fi",
            rating="PG-13",
            release_date=date(2010, 7, 16),
        )
        movie2 = Movie(
            title="Interstellar",
            description="ภารกิจค้นหาดาวเคราะห์ดวงใหม่",
            poster_url="https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
            duration_minutes=169,
            genre="Sci-Fi",
            rating="PG-13",
            release_date=date(2014, 11, 7),
        )
        db.add_all([movie1, movie2])
        db.flush()

        # ✦ Showtimes
        now = datetime.now(timezone.utc).replace(hour=10, minute=0, second=0, microsecond=0)
        showtimes = [
            Showtime(
                movie_id=movie1.id,
                cinema_id=cinema1.id,
                start_time=now + timedelta(hours=2),
                price=Decimal("220.00"),
            ),
            Showtime(
                movie_id=movie1.id,
                cinema_id=cinema2.id,
                start_time=now + timedelta(hours=5),
                price=Decimal("280.00"),
            ),
            Showtime(
                movie_id=movie2.id,
                cinema_id=cinema1.id,
                start_time=now + timedelta(days=1, hours=3),
                price=Decimal("220.00"),
            ),
        ]
        db.add_all(showtimes)

        db.commit()
        print("✅ Seed data inserted successfully!")
        print(f"   - Users: 2 (admin@movie.com / admin123, user@movie.com / user123)")
        print(f"   - Cinemas: 2")
        print(f"   - Movies: 2")
        print(f"   - Showtimes: {len(showtimes)}")
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
