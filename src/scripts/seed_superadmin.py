from src.config.database import SessionLocal
from src.models.user import User
from src.utils.security import hash_password

def seed_superadmin():
    db = SessionLocal()
    email = "superadmin@platform.com"
    existing = db.query(User).filter(User.email == email).first()
    if not existing:
        admin = User(
            name="Super Admin",
            email=email,
            phone="9999999999",
            password=hash_password("admin123"),
            is_superadmin=True
        )
        db.add(admin)
        db.commit()
        print("Superadmin created: email=superadmin@platform.com, password=admin123")
    else:
        existing.is_superadmin = True
        db.commit()
        print("User superadmin@platform.com updated to is_superadmin=True")
    db.close()

if __name__ == "__main__":
    seed_superadmin()
