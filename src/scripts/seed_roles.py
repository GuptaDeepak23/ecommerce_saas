from src.config.database import SessionLocal
from src.models.roles import Role

ROLES = [
    {
    "name" : "SUPERADMIN",
    "scope" : "PLATFORM",
    },
    {
     "name" : "OWNER",
     "scope" : "TENANT",
    },
    {
     "name" : "ADMIN",
     "scope" : "TENANT",
    },
    {
     "name" : "STAFF",
     "scope" : "TENANT",
    },
    {
     "name" : "CUSTOMER",
     "scope" : "PLATFORM",
    }
    
]

def seed_role():

    db = SessionLocal()

    for role in ROLES:
        existing_role = (db.query(Role).filter(Role.name == role["name"]).first())
        if not existing_role:
            db.add(Role(**role))
    db.commit()
    db.close()
    print("Roles seeded successfully")

if __name__ == "__main__":
    seed_role()
