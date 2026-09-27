from src.models.category import Category
from src.schemas.category import create_category , response_category , update_category
from src.config.database import dbsession
from fastapi import HTTPException


def find_category_by_name(db: dbsession, name: str, tenant_id: int):
    return db.query(Category).filter(
        Category.name == name,
        Category.tenant_id == tenant_id
    ).first()

def create_cat(db : dbsession , request : create_category , tenant_id: int):
    

    if find_category_by_name(db , request.name , tenant_id):
        raise HTTPException(status_code=400 , detail="Category with this name already exists")
    
    cat = Category(
         name = request.name,
         tenant_id = tenant_id
    )

    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

def get_cat(db , tenant_id: int):
    return db.query(Category).filter(Category.tenant_id == tenant_id).all()

def update_cat(db, id: int, request: update_category , tenant_id: int):
    cat = db.query(Category).filter(Category.id == id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")

    existing_cat = find_category_by_name(db, request.name , tenant_id)
    if existing_cat and existing_cat.id != id:
        raise HTTPException(status_code=400, detail="Category with this name already exists")

    cat.name = request.name
    db.commit()
    db.refresh(cat)
    return cat

def get_category_by_id(db , id:int , tenant_id: int):
    cat = db.query(Category).filter(Category.id == id , Category.tenant_id == tenant_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return cat
    
